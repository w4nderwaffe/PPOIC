import pytest

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

@pytest.fixture
def base_addresses():
    src = PostalAddress("Gedimino pr.", "10", "01103", "Vilnius", "Lithuania")
    dst = PostalAddress("Laisves al.", "25", "44311", "Kaunas", "Lithuania")
    return src, dst

@pytest.fixture
def base_service(base_addresses):
    src, dst = base_addresses
    domain = Domain(code="LT", name="Lithuania")
    config = ServerConfig(domain=domain, hub_id="HUB1")
    pricing = PricingEngine(
        tariffs=[
            Tariff(code="T_LOCAL", name="Local", base_price=1.5, price_per_kg=2.0, included_weight_kg=0.5, zone="local"),
            Tariff(code="T_NAT", name="National", base_price=3.0, price_per_kg=2.5, included_weight_kg=0.5, zone="national"),
            Tariff(code="T_INTL", name="Intl", base_price=8.0, price_per_kg=6.0, included_weight_kg=0.5, zone="international", priority=True),
        ],
        default_insurance=InsurancePlan(code="INS", max_cover_value=500.0, price_percent=1.0),
    )
    routing = RoutingEngine()
    sorting = SortingEngine()
    service = PostalService(config=config, pricing=pricing, routing=routing, sorting=sorting)

    off1 = PostOffice(id="OFF1", address=src)
    off2 = PostOffice(id="OFF2", address=dst)
    center = SortingCenter(id="HUB1", name="Vilnius HUB")
    service.register_office(off1, register=CashRegister(id="REG1"))
    service.register_office(off2, register=CashRegister(id="REG2"))
    service.register_center(center)
    return service
