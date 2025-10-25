import pytest

from postal_oop.items.AttachmentList import AttachmentList
from postal_oop.items.CustomsDeclaration import CustomsDeclaration
from postal_oop.items.Parcel import Parcel
from postal_oop.items.InsuredParcel import InsuredParcel
from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.core.Tariff import Tariff
from postal_oop.core.InsurancePlan import InsurancePlan
from postal_oop.core.Postmark import Postmark
from postal_oop.exceptions.OverweightError import OverweightError
from postal_oop.exceptions.OversizeError import OversizeError
from postal_oop.exceptions.InsufficientPostageError import InsufficientPostageError

from postal_oop.logistics.Courier import Courier
from postal_oop.logistics.Locker import Locker
from postal_oop.exceptions.LockerOccupiedError import LockerOccupiedError
from postal_oop.logistics.TransportUnit import TransportUnit
from postal_oop.logistics.Route import Route

from postal_oop.operations.Manifest import Manifest
from postal_oop.operations.Shipment import Shipment


def t(code="T", name="Nat", base=3.0, ppk=2.0, incl=0.5, zone="national"):
    return Tariff(code=code, name=name, base_price=base, price_per_kg=ppk, included_weight_kg=incl, zone=zone)


def addr(c="Vilnius"):
    return PostalAddress("Main", "1", "01103", c, "LT")


# --- AttachmentList coverage ---
def test_attachment_list_keywords_and_weight():
    att = AttachmentList(documents=["INV-1", "PACKING"])
    att.add("Gift book", 0.2)
    att.add("Chocolate box", 0.3)
    assert att.total_weight() == 0.5
    # должны попасть слова из items и documents
    kws = att.keywords()
    assert "gift" in kws and "inv-1" in kws


# --- PostalItem branches (oversize / overweight / postage) ---
def test_postal_item_limits_and_postage():
    # oversize
    big = Parcel(
        tracking_id="B1",
        sender=addr(),
        recipient=addr("Kaunas"),
        weight_kg=1.0,
        size_cm=(200, 120, 90),  # сильно больше лимитов
        stamps_value=10.0,
        tariff=t(),
    )
    with pytest.raises(OversizeError):
        big.check_limits()

    # overweight
    heavy = Parcel(
        tracking_id="H1",
        sender=addr(),
        recipient=addr("Kaunas"),
        weight_kg=100.0,  # больше 30 кг
        size_cm=(30, 20, 10),
        stamps_value=10.0,
        tariff=t(),
    )
    with pytest.raises(OverweightError):
        heavy.check_limits()

    # insufficient postage
    normal = Parcel(
        tracking_id="N1",
        sender=addr(),
        recipient=addr("Kaunas"),
        weight_kg=2.0,
        size_cm=(30, 20, 10),
        stamps_value=0.0,         # ничего не оплачено
        tariff=t(base=3.0, ppk=2.0, incl=0.5),
    )
    with pytest.raises(InsufficientPostageError):
        normal.verify_postage()


# --- Courier success path & movement ---
def test_courier_flow_success():
    cur = Courier(id="COK", full_name="Ok Courier")  # без unit — создастся дефолтный
    cur.assign_route(["OFF1", "OFF2"])
    assert cur.next_stop() == "OFF1"
    assert cur.advance() == "OFF1"
    assert cur.next_stop() == "OFF2"
    cur.load(5.0)
    cur.unload(2.0)
    # успешная доставка (recipient_present=True) — без исключения
    cur.attempt_delivery(addr(), recipient_present=True)


# --- Locker errors and happy path ---
def test_locker_put_pick_errors_and_ok():
    locker = Locker(id="L", location=addr(), max_weight_per_cell_kg=10.0)
    locker.add_cell("C1")
    locker.put("C1", "TRK1", 5.0)
    with pytest.raises(LockerOccupiedError):
        locker.put("C1", "TRK2", 1.0)  # занята
    assert locker.pickup("C1") == "TRK1"


# --- Route edge navigation ---
def test_route_navigation_edges():
    r = Route(id="R1", node_ids=["A", "B", "C"])
    # если текущего нет в списке — возвращает первый узел
    assert r.next_after("X") == "A"
    # нормальное продвижение
    assert r.next_after("A") == "B"
    assert r.total_hops() == 2


# --- Manifest: entries mode + shipments mode + mismatch ---
def test_manifest_entries_and_shipments_and_mismatch():
    # entries mode
    m = Manifest(id="M1")
    m.add_entry("TRK1", 1.5)
    m.add_entry("TRK2", 0.5)
    assert m.total_items() == 2
    assert m.total_weight() == 2.0
    assert m.has_tracking("TRK2") is True

    # shipments mode
    unit = TransportUnit(id="U", kind="van", max_load_kg=100.0)
    sh = Shipment(id="S1", route_id="R", unit=unit)
    sh.add_item("TRK3", 1.0)
    m2 = Manifest(id="M2", route_id="R")
    m2.add(sh)
    assert "S1" in m2.ids()
    assert m2.total_items() == 1
    assert m2.total_weight() == 1.0

    # mismatch
    sh2 = Shipment(id="S2", route_id="OTHER", unit=unit)
    with pytest.raises(ValueError):
        m2.add(sh2)


# --- InsuredParcel: declared_value from customs + insurance alias path ---
def test_insured_parcel_declared_from_customs_and_alias():
    base_kwargs = dict(
        tracking_id="INS1",
        sender=addr(),
        recipient=addr("Kaunas"),
        weight_kg=1.0,
        size_cm=(30, 20, 10),
        stamps_value=5.0,
        tariff=t(),
        declared_value=0.0,  # будет подставлено из customs.value_eur
    )

    ins = InsuredParcel(
        **base_kwargs,
        attachment=AttachmentList(
            documents=["INV-9"],
            customs=CustomsDeclaration(content_description="Gift", value_eur=50.0, country_of_origin="LT"),
        ),
        # alias branch: insurance (преобразуется в insurance_plan)
        insurance=InsurancePlan(code="INS", max_cover_value=100.0, price_percent=1.0),
    )
    # total_price не должен падать (declared_value взят из customs)
    assert ins.total_price() >= ins.base_price()
    # и claim_value ограничен покрытием
    assert ins.claim_value() == 50.0  # 50 <= max_cover
