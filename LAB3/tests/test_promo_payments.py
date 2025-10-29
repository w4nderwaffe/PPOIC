import pytest
from datetime import datetime, timedelta
from domain.promo.Coupon import Coupon
from domain.promo.Discount import Discount
from domain.promo.Promotion import Promotion
from domain.payments.PaymentGateway import PaymentGateway
from domain.payments.Payment import Payment
from domain.payments.Refund import Refund
from domain.payments.Wallet import Wallet
from domain.users.Customer import Customer
from domain.checkout.Order import Order
from exceptions.CouponExpiredException import CouponExpiredException
from exceptions.CouponUsageExceededException import CouponUsageExceededException
from exceptions.PaymentCaptureFailedException import PaymentCaptureFailedException
from exceptions.RefundNotAllowedException import RefundNotAllowedException
from exceptions.PaymentAuthorizationFailedException import PaymentAuthorizationFailedException

def test_coupon_and_discount_and_promo():
    c = Coupon(code="X", expiresAt=datetime.utcnow()+timedelta(days=1), maxUses=1)
    assert c.isValid(datetime.utcnow()) is True
    assert c.markUsed() == 0
    with pytest.raises(CouponUsageExceededException):
        c.markUsed()
    with pytest.raises(CouponExpiredException):
        Coupon(code="Y", expiresAt=datetime.utcnow()-timedelta(days=1), maxUses=1).isValid(datetime.utcnow())

    d = Discount(id=1, name="D", percentage=0.1)
    assert d.calculate(100.0) == pytest.approx(90.0)
    promo = Promotion(id=1, title="Black Friday", startsAt=datetime.utcnow()-timedelta(days=1))
    assert promo.isRunning(datetime.utcnow(), datetime.utcnow()+timedelta(days=1))

def test_payment_and_refund_and_wallet_flow():
    cust = Customer(userId=1)
    order = Order(id=1, customer=cust)
    pay = Payment(id=1, order=order, amount=200.0)
    gw = PaymentGateway(id=1, name="GW", configId="cfg")
    assert pay.capture(gw) is True

    ref = Refund(id=1, payment=pay, amount=50.0)
    assert ref.issue() is True
    assert ref.cancel() is True

    with pytest.raises(RefundNotAllowedException):
        Refund(id=2, payment=pay, amount=0.0).issue()

    w1 = Wallet(id=1, customer=cust, balance=100.0)
    w2 = Wallet(id=2, customer=cust, balance=0.0)
    w1.withdraw(40.0)
    w2.deposit(40.0)
    assert w1.balance == 60.0 and w2.balance == 40.0
    with pytest.raises(PaymentAuthorizationFailedException):
        w1.withdraw(1000.0)

def test_payment_capture_fail():
    cust = Customer(userId=2)
    order = Order(id=2, customer=cust)
    pay = Payment(id=2, order=order, amount=5000.0)
    gw = PaymentGateway(id=2, name="GW", configId="cfg")
    with pytest.raises(PaymentCaptureFailedException):
        pay.capture(gw)
