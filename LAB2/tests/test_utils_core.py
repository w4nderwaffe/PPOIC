from datetime import datetime
from postal_oop.utils import now, make_id, hash_text
from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.core.Person import Person
from postal_oop.core.Customer import Customer
from postal_oop.core.Postbox import Postbox
from postal_oop.core.Stamp import Stamp
from postal_oop.core.Postmark import Postmark
from postal_oop.core.Tariff import Tariff
from postal_oop.core.WeightBand import WeightBand
from postal_oop.core.InsurancePlan import InsurancePlan
from postal_oop.exceptions.AddressInvalidError import AddressInvalidError
from postal_oop.exceptions.OverweightError import OverweightError

def test_utils_now_make_id_hash():
    t = now()
    assert isinstance(t, datetime)
    mid = make_id("X")
    assert mid.startswith("X_") and len(mid) > 3
    assert hash_text("abc") != hash_text("abcd")

def test_postal_address_validate_and_format():
    a = PostalAddress("Street", "1", "01103", "Vilnius", "LT")
    a.validate()
    assert "Street" in a.formatted()
    b = PostalAddress("Other", "2", "01104", "Vilnius", "LT")
    assert a.same_city(b)
    try:
        PostalAddress("", "", "abc", "", "").validate()
        assert False
    except AddressInvalidError:
        pass

def test_person_and_customer():
    p = Person("Ivanov Ivan Ivanovich", phone="+111")
    assert p.short_name().startswith("Ivanov")
    c = Customer("John Doe")
    c.add_points(10)
    assert c.loyalty_points == 10
    c.set_preference("notify", "sms")
    assert c.prefers_office(None) is False

def test_postbox_receive_and_pickup():
    import math
    pb = Postbox(id="PB1", address=PostalAddress("S","1","01103","Vilnius","LT"), max_items=3, max_weight_kg=1.0)
    pb.receive_item(0.3)
    pb.receive_item(0.3)
    assert math.isclose(pb.load_factor(), 2/3, rel_tol=1e-6)
    try:
        pb.receive_item(0.5)
    except OverweightError:
        pass
    total = pb.pickup(1)
    assert total > 0

def test_stamp_and_postmark():
    from datetime import date
    st = Stamp(code="A", face_value=1.0, country="LT", issued_on=date.today())
    assert st.value_left() == 1.0
    st.cancel()
    assert st.value_left() == 0.0
    pm = Postmark(office_id="OFF1", country="LT", code="001", stamped_at=now())
    assert "POSTMARK" in pm.apply_to_text("x")
    assert isinstance(pm.is_older_than(0), bool)

def test_tariff_weightband_insurance():
    t = Tariff(code="T", name="X", base_price=2.0, price_per_kg=1.0, included_weight_kg=0.5, zone="local")
    assert t.estimate(0.2) == 2.0
    assert t.estimate(1.5) == 3.0
    b = WeightBand(max_weight_kg=2.0, label="S")
    assert b.fits(1.9)
    ins = InsurancePlan(code="I", max_cover_value=100.0, price_percent=2.0, min_price=1.0)
    assert ins.premium(10.0) == 1.0
    assert ins.premium(100.0) == 2.0
    assert ins.can_cover(50.0)
