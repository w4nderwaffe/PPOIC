import pytest
from domain.comm.EmailMessage import EmailMessage
from domain.comm.SMSMessage import SMSMessage
from domain.comm.PushMessage import PushMessage
from domain.comm.Notification import Notification
from domain.support.SupportTicket import SupportTicket
from domain.support.ChatMessage import ChatMessage
from domain.loyalty.Recommendation import Recommendation
from domain.loyalty.Wishlist import Wishlist
from domain.loyalty.PointsTransaction import PointsTransaction
from domain.users.User import User
from domain.users.Customer import Customer
from domain.catalog.Product import Product

def test_comm_messages_and_notifications():
    em = EmailMessage(id=1, toAddress="a@b", subject="Hi")
    txt = em.render("Hello {name}", {"name":"Alice"})
    assert "Alice" in txt
    assert em.dispatch() is True

    sms = SMSMessage(id=1, toNumber="+370", text="x"*200)
    truncated = sms.truncateIfNeeded(160)
    assert len(truncated) == 160
    assert sms.dispatch() is True

    pm = PushMessage(id=1, deviceToken="tok", payload={})
    pm.enrichPayload({"k":"v"})
    assert pm.payload.get("k") == "v"
    assert pm.dispatch() is True

    u = User(id=1, email="x", role="user")
    n = Notification(id=1, user=u, channel="email")
    assert n.send() and n.markRead()

def test_support_and_loyalty():
    cust = Customer(userId=1)
    t = SupportTicket(id=1, customer=cust)
    msg = ChatMessage(id=1, ticket=t, authorId=1)
    red = msg.redactPII("my phone 12345")
    assert "#" in red
    assert t.addMessage(msg) is True
    assert t.close() is True

    rec = Recommendation(id=1, customer=cust, algorithm="popular")
    catalog = [Product(id=i, name=f"P{i}", category=None) for i in range(5)]
    top3 = rec.generate(catalog)
    assert len(top3) == 3
    assert rec.acceptFeedback(5) is True

    wl = Wishlist(id=1, customer=cust, name="Default")
    p = Product(id=99, name="X", category=None)
    assert wl.addProduct(p) and wl.removeProduct(p)
    pt = PointsTransaction(id=1, loyaltyAccountId=1, delta=10)
    assert pt.apply() == 10 and pt.revert() == -10
