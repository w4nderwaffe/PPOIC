from __future__ import annotations
from dataclasses import asdict
from typing import List, Tuple

# Import package modules
from postal_oop.services.PostalService import PostalService
from postal_oop.domain.Domain import Domain
from postal_oop.domain.ServerConfig import ServerConfig
from postal_oop.engines.PricingEngine import PricingEngine
from postal_oop.engines.SortingEngine import SortingEngine
from postal_oop.engines.RoutingEngine import RoutingEngine

from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.core.Tariff import Tariff
from postal_oop.core.WeightBand import WeightBand

from postal_oop.items.Letter import Letter
from postal_oop.items.Parcel import Parcel
from postal_oop.items.RegisteredLetter import RegisteredLetter
from postal_oop.items.InsuredParcel import InsuredParcel

from postal_oop.operations.TrackingId import TrackingId
from postal_oop.operations.TrackingEvent import TrackingEvent
from postal_oop.operations.CashRegister import CashRegister

from postal_oop.logistics.PostOffice import PostOffice
from postal_oop.logistics.SortingCenter import SortingCenter
from postal_oop.logistics.Courier import Courier


def banner(title: str):
    print("\n" + "="*12, title, "="*12)


def build_service() -> PostalService:
    # Domain with one office and one central hub
    domain = Domain(code="LT", name="Lithuania")
    domain.add_office("VNO-01")
    domain.add_center("HUB-VNO")

    config = ServerConfig(domain=domain, hub_id="HUB-VNO")

    # Basic tariffs and bands
    tariffs = [
        Tariff(code="LOC-STD", name="Local Standard", base_price=2.0, price_per_kg=0.0, included_weight_kg=1.0, zone="local"),
        Tariff(code="NAT-STD", name="National Standard", base_price=4.5, price_per_kg=0.8, included_weight_kg=1.0, zone="national"),
        Tariff(code="INT-STD", name="International Standard", base_price=9.0, price_per_kg=2.5, included_weight_kg=0.5, zone="international"),
        Tariff(code="NAT-EXP", name="National Express", base_price=8.0, price_per_kg=1.2, included_weight_kg=1.0, zone="national", priority=True),
    ]
    bands = [
        WeightBand(max_weight_kg=0.5, label="XS"),
        WeightBand(max_weight_kg=1.0, label="S"),
        WeightBand(max_weight_kg=5.0, label="M"),
        WeightBand(max_weight_kg=20.0, label="L"),
    ]
    pricing = PricingEngine(tariffs=tariffs, bands=bands)

    service = PostalService(
        config=config,
        pricing=pricing,
        sorting=SortingEngine(),
        routing=RoutingEngine(),
        # notifiers use defaults via factory; you can override here if needed
    )
    return service


def demo_flow():
    svc = build_service()

    # Register office (with cash register) and hub center
    office_addr = PostalAddress(street="Gedimino pr.", house="1", postal_code="LT-01103", city="Vilnius", country="LT", apartment=None)
    office = PostOffice(id="VNO-01", address=office_addr, services={"letter","parcel"})
    register = CashRegister(id="REG-01", opened=True, balance=100.0)  # open shift with float
    svc.register_office(office, register=register)

    center = SortingCenter(id="HUB-VNO", name="Vilnius Central Hub")
    svc.register_center(center)

    # Sender/Recipient addresses
    sender = PostalAddress(street="Aukštaičių g.", house="10", postal_code="LT-01234", city="Vilnius", country="LT")
    recipient = PostalAddress(street="Laisvės al.", house="5", postal_code="LT-50000", city="Kaunas", country="LT")

    # Build items with Tracking IDs
    # Select zone using config to pick tariff
    # compute zone
    same_city = sender.city.strip().lower() == recipient.city.strip().lower()
    zone = 'local' if same_city else ('national' if sender.country.strip().lower()==recipient.country.strip().lower() else 'international')
    tariff_letter = svc.pricing.pick_tariff(zone=zone, priority=False) or svc.pricing.tariffs[0]
    tariff_parcel = svc.pricing.pick_tariff(zone=zone, priority=True) or svc.pricing.tariffs[0]

    tid1 = TrackingId.new("LTR").normalized()
    tid2 = TrackingId.new("PAR").normalized()

    letter = RegisteredLetter(tracking_id=tid1, sender=sender, recipient=recipient,
                               weight_kg=0.2, size_cm=(20.0,15.0,0.2), stamps_value=0.0,
                               tariff=tariff_letter, declared_value=10.0)
    parcel = Parcel(tracking_id=tid2, sender=sender, recipient=recipient,
                    weight_kg=2.3, size_cm=(40.0,30.0,20.0), stamps_value=0.0,
                    tariff=tariff_parcel, declared_value=120.0)

    banner("QUOTES")
    q1 = svc.quote(letter, priority=False, insure=False)
    q2 = svc.quote(parcel, priority=True, insure=False)
    print("RegisteredLetter quote:", q1)
    print("Parcel (priority) quote:", q2)

    banner("REGISTER ITEMS")
    svc.register_item(letter)
    svc.register_item(parcel)

    banner("ACCEPT AT OFFICE (PAY)")
    total1 = svc.accept_at_office(office_id="VNO-01", item=letter, take_payment=True)
    total2 = svc.accept_at_office(office_id="VNO-01", item=parcel, take_payment=True)
    print("Paid totals:", total1, total2)

    # Issue receipt (simple sample lines)
    lines: list[tuple[str, float]] = [(f"RegisteredLetter {tid1}", total1), (f"Parcel {tid2}", total2)]
    receipt = svc.issue_receipt(office_id="VNO-01", payment_id="PAY-0001", lines=lines, footer="Спасибо за отправку!")
    print("Receipt:", receipt)

    banner("HANDOVER TO HUB")
    svc.handover_to_center(center_id="HUB-VNO", item=letter)
    svc.handover_to_center(center_id="HUB-VNO", item=parcel)

    banner("PLAN ROUTE")
    route1 = svc.plan_route(source_office_id="VNO-01", dest_office_id="VNO-01", item=letter)
    route2 = svc.plan_route(source_office_id="VNO-01", dest_office_id="VNO-01", item=parcel)
    print("Route LTR:", route1)
    print("Route PAR:", route2)

    banner("COURIER DELIVERY")
    courier = Courier(id="CR-7", name="Jonas Jonaitis", full_name="Jonas Jonaitis")
    svc.deliver_by_courier(courier=courier, item=letter, recipient_present=True)
    svc.deliver_by_courier(courier=courier, item=parcel, recipient_present=True)

    banner("TRACKING HISTORY")
    for tid in (tid1, tid2):
        hist = svc.history(tid)
        print(f"{tid}:")
        for e in hist:
            print("  ", e.status, "@", e.location_node_id, "|", e.timestamp.isoformat())

    banner("NOTIFY (EMAIL/SMS/PUSH)")
    contact = {"email": "user@example.com", "phone": "+37060000000", "push": "user-device-token"}
    res = svc.notify_all(contact, tracking_id=tid2, status="DELIVERED")
    print("Notify results:", res)


if __name__ == "__main__":
    demo_flow()
