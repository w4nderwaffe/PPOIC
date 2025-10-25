from postal_oop.logistics.PostOffice import PostOffice
from postal_oop.logistics.SortingCenter import SortingCenter
from postal_oop.logistics.Route import Route
from postal_oop.logistics.TransportUnit import TransportUnit
from postal_oop.logistics.Truck import Truck
from postal_oop.logistics.Van import Van
from postal_oop.logistics.TrainCar import TrainCar
from postal_oop.logistics.AirFreight import AirFreight
from postal_oop.logistics.Courier import Courier
from postal_oop.logistics.CourierRoutePlan import CourierRoutePlan
from postal_oop.logistics.Locker import Locker

from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.items.Letter import Letter
from postal_oop.core.Tariff import Tariff
from postal_oop.exceptions.DeliveryAttemptFailedError import DeliveryAttemptFailedError

def test_post_office_and_center_and_route():
    off = PostOffice(id="OFF1", address=PostalAddress("S","1","01103","Vilnius","LT"))
    lt = Letter(
        tracking_id="T",
        sender=off.address,
        recipient=PostalAddress("R","1","44311","Kaunas","LT"),
        weight_kg=0.2,
        size_cm=(20,10,1),
        stamps_value=2.0,
        tariff=Tariff(code="TN", name="Nat", base_price=3.0, price_per_kg=2.5, included_weight_kg=0.5, zone="national"),
    )
    assert off.accept_item(lt) >= 0

    sc = SortingCenter(id="HUB1", name="HUB")
    sc.enqueue(lt)
    assert sc.queue_size() == 1

    r = Route(id="R1", node_ids=["OFF1","HUB1","OFF2"])
    unit = TransportUnit(id="U", kind="van", max_load_kg=500.0)
    tr = Truck(id="TR", plate="AAA-111", unit=unit)

    v = Van(id="V1", plate="BBB-222", unit=TransportUnit(id="UV", kind="van", max_load_kg=200.0))
    tc = TrainCar(id="C1", number="C-01", unit=TransportUnit(id="UC", kind="railcar", max_load_kg=2000.0))
    af = AirFreight(id="AF1", flight="AB123", unit=TransportUnit(id="UA", kind="air", max_load_kg=5000.0))

    assert tr.unit.max_load_kg == 500.0
    assert v.unit.kind == "van"
    assert tc.unit.kind == "railcar"
    assert af.unit.kind == "air"

    cur = Courier(id="C", name="Joe", unit=TransportUnit(id="UCUR", kind="bike", max_load_kg=30.0))
    plan = CourierRoutePlan(courier_id=cur.id, stops=["OFF1","OFF2"])
    cur.assign_route([plan.stops[0]])
    assert cur.next_stop() is not None
    cur.load(5.0); cur.unload(2.0)

    try:
        cur.attempt_delivery(PostalAddress("S","1","01103","Vilnius","LT"), recipient_present=False)
        assert False
    except DeliveryAttemptFailedError:
        pass

    locker = Locker(id="L1", location=PostalAddress("S","1","01103","Vilnius","LT"), max_weight_per_cell_kg=10.0)
    locker.add_cell("C1")
    locker.put("C1", "TRK", 5.0)
    tid = locker.pickup("C1")
    assert tid == "TRK"
