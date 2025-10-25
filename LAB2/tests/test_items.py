import pytest
from postal_oop.items.PostalItem import PostalItem
from postal_oop.items.Letter import Letter
from postal_oop.items.RegisteredLetter import RegisteredLetter
from postal_oop.items.Postcard import Postcard
from postal_oop.items.Parcel import Parcel
from postal_oop.items.SmallPackage import SmallPackage
from postal_oop.items.FragileParcel import FragileParcel
from postal_oop.items.OversizedParcel import OversizedParcel
from postal_oop.items.CODParcel import CODParcel
from postal_oop.items.InsuredParcel import InsuredParcel
from postal_oop.items.AttachmentList import AttachmentList
from postal_oop.items.CustomsDeclaration import CustomsDeclaration

from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.core.Postmark import Postmark
from postal_oop.core.Tariff import Tariff
from postal_oop.core.InsurancePlan import InsurancePlan
from postal_oop.utils import now

from postal_oop.exceptions.InsufficientPostageError import InsufficientPostageError

def base_item():
    return Parcel(
        tracking_id="TRK0001",
        sender=PostalAddress("S","1","01103","Vilnius","LT"),
        recipient=PostalAddress("R","2","44311","Kaunas","LT"),
        weight_kg=1.0,
        size_cm=(30,20,10),
        stamps_value=5.0,
        tariff=Tariff(code="T1", name="Nat", base_price=3.0, price_per_kg=2.5, included_weight_kg=0.5, zone="national"),
    )

def test_postal_item_price_and_limits():
    item = base_item()
    item.add_postmark(Postmark(office_id="OFF1", country="LT", code="001", stamped_at=now()))
    assert isinstance(item, PostalItem)
    assert item.total_price() >= item.base_price()
    assert item.verify_postage() is None

def test_insufficient_postage():
    item = base_item()
    item.stamps_value = 0.0
    with pytest.raises(InsufficientPostageError):
        item.verify_postage()

def test_letter_registered_postcard_packages():
    l = Letter(
        tracking_id="X",
        sender=PostalAddress("S","1","01103","Vilnius","LT"),
        recipient=PostalAddress("R","1","01103","Vilnius","LT"),
        weight_kg=0.2,
        size_cm=(20,10,1),
        stamps_value=2.0,
        tariff=Tariff(code="TL", name="Local", base_price=1.5, price_per_kg=2.0, included_weight_kg=0.5, zone="local"),
    )
    r = RegisteredLetter(**{**l.__dict__})
    assert r.total_price() >= l.total_price()

    pc = Postcard(
        tracking_id="PC",
        sender=l.sender,
        recipient=l.recipient,
        stamps_value=1.5,
        tariff=Tariff(code="TL", name="Local", base_price=1.0, price_per_kg=2.0, included_weight_kg=0.5, zone="local"),
    )
    assert pc.total_price() >= 1.0

    sp = SmallPackage(
        tracking_id="SP",
        sender=l.sender,
        recipient=l.recipient,
        weight_kg=1.2,
        size_cm=(20,15,10),
        stamps_value=3.0,
        tariff=Tariff(code="TN", name="Nat", base_price=3.0, price_per_kg=2.5, included_weight_kg=0.5, zone="national"),
    )
    fp = FragileParcel(**{**sp.__dict__})
    assert fp.total_price() > sp.total_price()
    oz = OversizedParcel(**{**sp.__dict__})
    assert oz.total_price() > sp.total_price()

def test_cod_and_insured_parcels():
    base = base_item()
    cod = CODParcel(**{**base.__dict__}, cod_amount=20.0)
    assert cod.total_price() >= base.total_price()

    ins = InsuredParcel(
        **{**base.__dict__},
        attachment=AttachmentList(
            documents=["INV-1", "PACKING"],
            customs=CustomsDeclaration(
                content_description="Gift",
                value_eur=50.0,
                country_of_origin="LT"
            ),
        ),
        insurance=InsurancePlan(code="INS", max_cover_value=500.0, price_percent=1.0),
    )
    assert ins.total_price() >= base.total_price()
