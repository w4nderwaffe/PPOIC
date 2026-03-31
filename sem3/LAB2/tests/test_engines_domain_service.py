from postal_oop.items.Letter import Letter
from postal_oop.items.CODParcel import CODParcel
from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.core.Tariff import Tariff
from postal_oop.core.InsurancePlan import InsurancePlan
from postal_oop.domain.Domain import Domain
from postal_oop.domain.ServerConfig import ServerConfig
from postal_oop.engines.PricingEngine import PricingEngine
from postal_oop.engines.RoutingEngine import RoutingEngine
from postal_oop.engines.SortingEngine import SortingEngine
from postal_oop.services.PostalService import PostalService
from postal_oop.logistics.PostOffice import PostOffice
from postal_oop.logistics.SortingCenter import SortingCenter
from postal_oop.operations.CashRegister import CashRegister

def test_pricing_routing_sorting_and_domain():
    pricing = PricingEngine(
        tariffs=[
            Tariff(code="TL", name="Local", base_price=1.0, price_per_kg=1.0, included_weight_kg=0.5, zone="local"),
            Tariff(code="TN", name="Nat", base_price=3.0, price_per_kg=2.0, included_weight_kg=0.5, zone="national"),
        ]
    )
    letter = Letter(tracking_id="T", sender=PostalAddress("A","1","01103","Vilnius","LT"), recipient=PostalAddress("B","1","44311","Kaunas","LT"), weight_kg=0.3, size_cm=(20,10,1), stamps_value=5.0, tariff=pricing.tariffs[1])
    assert pricing.calculate(letter, zone="national") >= 3.0

    re = RoutingEngine()
    rt = re.plan("OFF1","OFF2", letter.sender, letter.recipient)
    assert rt.nodes[0] == "OFF1"

    se = SortingEngine()
    assert se.barcode_ok("ABC12345")
    node = se.choose_center(letter, ["HUB1","HUB2"])
    assert node in {"HUB1","HUB2"}

    d = Domain(code="LT", name="Lithuania")
    d.add_office("OFF1"); d.add_center("HUB1")
    cfg = ServerConfig(domain=d, hub_id="HUB1")
    assert cfg.is_local_route("Vilnius","Vilnius")
    z = cfg.zone_for("LT","LT", same_city=False)
    assert z == "national"

def test_postal_service_flow(base_service):
    service = base_service
    letter = Letter(tracking_id="TRK123", sender=service.offices["OFF1"].address, recipient=service.offices["OFF2"].address, weight_kg=0.2, size_cm=(20,10,1), stamps_value=5.0, tariff=service.pricing.tariffs[1])
    service.register_item(letter)
    q = service.quote(letter)
    assert q >= 3.0
    service.accept_at_office("OFF1", letter)
    route = service.plan_route("OFF1","OFF2", letter)
    assert route.nodes[-1] == "OFF2"
    service.handover_to_center("HUB1", letter)

    from postal_oop.logistics.Courier import Courier
    cur = Courier(full_name="A", id="C1")
    service.deliver_by_courier(cur, letter, recipient_present=True)
    hist = service.history(letter.tracking_id)
    assert any(ev.status == "DELIVERED" for ev in hist)

def test_cod_flow(base_service):
    service = base_service
    cod = CODParcel(tracking_id="TRKCOD", sender=service.offices["OFF1"].address, recipient=service.offices["OFF2"].address, weight_kg=1.0, size_cm=(30,20,10), stamps_value=5.0, tariff=service.pricing.tariffs[1], cod_amount=10.0)
    service.register_item(cod)
    service.accept_at_office("OFF1", cod)
    service.handover_to_center("HUB1", cod)
    from postal_oop.logistics.Courier import Courier
    cur = Courier(full_name="A", id="C2")
    service.deliver_by_courier(cur, cod, recipient_present=True)
    hist = service.history("TRKCOD")
    assert any(ev.status == "DELIVERED" for ev in hist)
