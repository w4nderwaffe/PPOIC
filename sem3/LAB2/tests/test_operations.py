from postal_oop.operations.Shipment import Shipment
from postal_oop.operations.Manifest import Manifest
from postal_oop.operations.TrackingId import TrackingId
from postal_oop.operations.TrackingEvent import TrackingEvent
from postal_oop.operations.CashRegister import CashRegister
from postal_oop.operations.Payment import Payment
from postal_oop.operations.Receipt import Receipt
from postal_oop.operations.QueueTicket import QueueTicket

from postal_oop.logistics.TransportUnit import TransportUnit

def test_shipment_and_manifest():
    unit = TransportUnit(id="U", kind="van", max_load_kg=100.0)
    sh = Shipment(id="S", route_id="R", unit=unit)
    sh.add_item("TRK1", 10.0)
    sh.depart("OFF1"); sh.arrive("OFF2")
    m = Manifest(id="M", shipment_id=sh.id)
    m.add_entry("TRK1", 10.0)
    assert m.total_weight() == 10.0
    assert m.has_tracking("TRK1")

def test_tracking_and_cash_and_payment_and_receipt_and_queue():
    tid = TrackingId.new().normalized()
    ev = TrackingEvent(tracking_id=tid, status="CREATED", location_node_id="CLIENT")
    assert not ev.is_final()
    reg = CashRegister(id="REG1")
    reg.open_shift(10.0)
    p = Payment(id="P1", amount=5.0, currency="EUR", method="cash")
    p.authorize(); assert p.approved
    reg.accept_payment(p.id, p.amount, p.method)
    r = Receipt(id="R1", payment_id=p.id)
    r.add_item("Service", 5.0)
    assert "TOTAL" in r.render_text()
    qt = QueueTicket(office_id="OFF1", number=1)
    assert qt.code().startswith("OFF1-")
    reg.refund("P1", 2.0)
