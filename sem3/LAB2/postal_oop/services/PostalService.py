from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.core.Tariff import Tariff
from postal_oop.core.InsurancePlan import InsurancePlan

from postal_oop.items.PostalItem import PostalItem
from postal_oop.items.CODParcel import CODParcel

from postal_oop.logistics.PostOffice import PostOffice
from postal_oop.logistics.SortingCenter import SortingCenter
from postal_oop.logistics.Route import Route
from postal_oop.logistics.Courier import Courier

from postal_oop.operations.TrackingEvent import TrackingEvent
from postal_oop.operations.CashRegister import CashRegister
from postal_oop.operations.Payment import Payment
from postal_oop.operations.Receipt import Receipt

from postal_oop.engines.PricingEngine import PricingEngine
from postal_oop.engines.RoutingEngine import RoutingEngine
from postal_oop.engines.SortingEngine import SortingEngine

from postal_oop.domain.ServerConfig import ServerConfig

from postal_oop.notifications.SMSNotifier import SMSNotifier
from postal_oop.notifications.EmailNotifier import EmailNotifier
from postal_oop.notifications.PushNotifier import PushNotifier

from postal_oop.exceptions.TrackingNotFoundError import TrackingNotFoundError
from postal_oop.exceptions.DuplicateTrackingError import DuplicateTrackingError
from postal_oop.exceptions.InsufficientPostageError import InsufficientPostageError

@dataclass
class PostalService:
    config: ServerConfig
    pricing: PricingEngine
    routing: RoutingEngine
    sorting: SortingEngine

    offices: Dict[str, PostOffice] = field(default_factory=dict)
    centers: Dict[str, SortingCenter] = field(default_factory=dict)
    registers: Dict[str, CashRegister] = field(default_factory=dict)

    track_events: Dict[str, List[TrackingEvent]] = field(default_factory=dict)
    registry_items: Dict[str, PostalItem] = field(default_factory=dict)

    sms: SMSNotifier = field(default_factory=SMSNotifier)
    email: EmailNotifier = field(default_factory=EmailNotifier)
    push: PushNotifier = field(default_factory=PushNotifier)

    def register_office(self, office: PostOffice, register: Optional[CashRegister] = None) -> None:
        self.offices[office.id] = office
        self.config.domain.add_office(office.id)
        if register:
            self.registers[office.id] = register

    def register_center(self, center: SortingCenter) -> None:
        self.centers[center.id] = center
        self.config.domain.add_center(center.id)

    # ----------- Трекинг -----------
    def _ensure_tracking(self, tracking_id: str) -> None:
        if tracking_id not in self.track_events:
            self.track_events[tracking_id] = []

    def add_event(self, e: TrackingEvent) -> None:
        self._ensure_tracking(e.tracking_id)
        self.track_events[e.tracking_id].append(e)

    def history(self, tracking_id: str) -> List[TrackingEvent]:
        if tracking_id not in self.track_events:
            raise TrackingNotFoundError(tracking_id)
        return list(self.track_events[tracking_id])

    # ----------- Регистрация отправления -----------
    def register_item(self, item: PostalItem) -> None:
        if item.tracking_id in self.registry_items:
            raise DuplicateTrackingError(item.tracking_id)
        self.registry_items[item.tracking_id] = item
        self.add_event(TrackingEvent(tracking_id=item.tracking_id, status="CREATED", location_node_id="CLIENT"))

    # ----------- Расчёт стоимости -----------
    def quote(self, item: PostalItem, priority: bool = False, insure: bool = False) -> float:
        zone = self.config.zone_for(item.sender.country, item.recipient.country, item.sender.same_city(item.recipient))
        return self.pricing.calculate(item, zone=zone, priority=priority, insure=insure)

    # ----------- Приём в отделении -----------
    def accept_at_office(self, office_id: str, item: PostalItem, take_payment: bool = False) -> float:
        office = self.offices.get(office_id)
        if not office:
            raise ValueError("Неизвестное отделение")
        # Проверим, достаточно ли оплачено марками
        try:
            item.verify_postage()
        except InsufficientPostageError:
            if not take_payment:
                raise
            # Если надо — пробиваем платёж через кассу отделения
            need = item.total_price()
            reg = self.registers.get(office_id)
            if not reg:
                raise RuntimeError("В отделении нет кассы")
            pay = Payment(id=f"PAY_{item.tracking_id}", amount=need, currency="EUR", method="cash")
            pay.authorize()
            if not pay.approved:
                raise RuntimeError("Платёж не авторизован")
            reg.accept_payment(pay.id, pay.amount, pay.method)
        # Принято
        office.accept_item(item)
        self.add_event(TrackingEvent(tracking_id=item.tracking_id, status="ACCEPTED", location_node_id=office_id))
        return item.total_price()

    # ----------- Маршрутизация -----------
    def plan_route(self, source_office_id: str, dest_office_id: str, item: PostalItem) -> Route:
        src = item.sender
        dst = item.recipient
        if not (self.config.knows_office(source_office_id) and self.config.knows_office(dest_office_id)):
            raise ValueError("Неизвестные узлы маршрута")
        route = self.routing.plan(source_office_id, dest_office_id, src, dst)
        return route

    def handover_to_center(self, center_id: str, item: PostalItem) -> None:
        center = self.centers.get(center_id)
        if not center:
            raise ValueError("Неизвестный сортировочный центр")
        center.enqueue(item)
        self.add_event(TrackingEvent(tracking_id=item.tracking_id, status="SORTED", location_node_id=center_id))

    # ----------- Доставка курьером -----------
    def deliver_by_courier(self, courier: Courier, item: PostalItem, recipient_present: bool) -> None:
        # Если наложенный платёж — проверим перед вручением
        if isinstance(item, CODParcel) and item.requires_cod():
            # учебно: курьер принимает ровно сумму (без наличной кассы)
            item.collect_cod(paid_amount=item.cod_amount)
        courier.attempt_delivery(item.recipient, recipient_present=recipient_present)
        self.add_event(TrackingEvent(tracking_id=item.tracking_id, status="DELIVERED", location_node_id="COURIER"))

    # ----------- Уведомления -----------
    def notify_all(self, contact: dict, tracking_id: str, status: str) -> Dict[str, Optional[str]]:
        """contact: {'phone': str|None, 'email': str|None, 'token': str|None}"""
        res: Dict[str, Optional[str]] = {"sms": None, "email": None, "push": None}
        if phone := contact.get("phone"):
            res["sms"] = self.sms.send_status_update(phone, tracking_id, status)
        if email := contact.get("email"):
            res["email"] = self.email.send_status_update(email, tracking_id, status)
        if token := contact.get("token"):
            res["push"] = self.push.send_status_update(token, tracking_id, status)
        return res

    # ----------- Печать чека -----------
    def issue_receipt(self, office_id: str, payment_id: str, lines: List[tuple[str, float]], footer: str = "Спасибо!") -> Receipt:
        rec = Receipt(id=f"R_{payment_id}", payment_id=payment_id, footer_note=footer)
        for d, p in lines:
            rec.add_item(d, p)
        return rec
