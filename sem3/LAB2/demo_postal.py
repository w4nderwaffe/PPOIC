# demo_postal.py
# Мини-демо для пакета физической почты `postal_oop`.
# Запуск: python3 demo_postal.py  (из директории, где лежит папка postal_oop)

from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.core.Tariff import Tariff
from postal_oop.core.InsurancePlan import InsurancePlan
from postal_oop.domain.Domain import Domain
from postal_oop.domain.ServerConfig import ServerConfig

from postal_oop.logistics.PostOffice import PostOffice
from postal_oop.logistics.SortingCenter import SortingCenter
from postal_oop.logistics.Courier import Courier

from postal_oop.engines.PricingEngine import PricingEngine
from postal_oop.engines.RoutingEngine import RoutingEngine
from postal_oop.engines.SortingEngine import SortingEngine

from postal_oop.services.PostalService import PostalService

from postal_oop.operations.CashRegister import CashRegister
from postal_oop.operations.TrackingEvent import TrackingEvent

from postal_oop.items.Letter import Letter


def main() -> None:
    # --- 1) Базовая конфигурация сети ---
    domain = Domain(code="LT", name="Lithuania")
    config = ServerConfig(domain=domain, hub_id="HUB1")

    pricing = PricingEngine(
        tariffs=[
            Tariff(code="T_LOCAL", name="Local", base_price=1.50, price_per_kg=2.00, included_weight_kg=0.5, zone="local"),
            Tariff(code="T_NAT",   name="National", base_price=3.00, price_per_kg=2.50, included_weight_kg=0.5, zone="national"),
            Tariff(code="T_INTL",  name="International", base_price=8.00, price_per_kg=6.00, included_weight_kg=0.5, zone="international", priority=True),
        ],
        default_insurance=InsurancePlan(code="INS", max_cover_value=500.0, price_percent=1.0),
    )

    routing = RoutingEngine()
    sorting = SortingEngine()

    service = PostalService(config=config, pricing=pricing, routing=routing, sorting=sorting)

    # --- 2) Узлы сети: отделения и сортировочный центр ---
    office_A = PostOffice(
        id="OFF1",
        address=PostalAddress("Gedimino pr.", "10", "01103", "Vilnius", "Lithuania")
    )
    office_B = PostOffice(
        id="OFF2",
        address=PostalAddress("Laisves al.", "25", "44311", "Kaunas", "Lithuania")
    )
    hub = SortingCenter(id="HUB1", name="Vilnius Sorting Center")

    service.register_office(office_A, register=CashRegister(id="REG1"))
    service.register_office(office_B, register=CashRegister(id="REG2"))
    service.register_center(hub)

    # --- 3) Отправление: письмо ---
    letter = Letter(
        tracking_id="TRK123456",                 # a-zA-Z0-9, длина 8..32 — подходит
        sender=office_A.address,
        recipient=office_B.address,
        weight_kg=0.20,
        size_cm=(20.0, 10.0, 0.2),
        stamps_value=2.00,                       # марок приклеено на сумму
    )

    # Регистрация в системе (получим первое событие CREATED)
    service.register_item(letter)

    # Оценка тарифа по зоне (между городами в одной стране → national)
    cost = service.quote(letter, priority=False, insure=False)
    print(f"Тариф: {cost:.2f} EUR")

    # --- 4) Приём в отделении источника ---
    # Если марок не хватает, accept_at_office возьмёт оплату через кассу (у нас хватает).
    service.accept_at_office("OFF1", letter)

    # --- 5) План маршрута и передача в сортировочный центр ---
    route = service.plan_route("OFF1", "OFF2", letter)
    print("Маршрут:", route.nodes)

    # Передаём на сортировку (получим событие SORTED)
    service.handover_to_center("HUB1", letter)

    # --- 6) Доставка курьером до получателя ---
    courier = Courier(full_name="Jonas Jonaitis", id="C1", phone="+37060000000")
    courier.load(letter.weight_kg)  # опционально, имитация загрузки
    service.deliver_by_courier(courier=courier, item=letter, recipient_present=True)

    # --- 7) Уведомление получателя (опционально, можно убрать) ---
    notify_ids = service.notify_all(
        contact={"phone": "+37060000000", "email": "user@example.com", "token": "device_token_12345"},
        tracking_id=letter.tracking_id,
        status="DELIVERED",
    )
    print("Уведомления отправлены:", notify_ids)

    # --- 8) История трекинга ---
    print("\nИстория:")
    for ev in service.history(letter.tracking_id):
        print(f"{ev.status} @ {ev.location_node_id} — {ev.timestamp.isoformat(timespec='seconds')}")

    print("\n✅ Почтовое отправление доставлено.")


if __name__ == "__main__":
    main()
