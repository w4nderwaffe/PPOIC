from domain.users.User import User
from domain.security.PasswordPolicy import PasswordPolicy
from domain.security.AuthService import AuthService
from domain.users.Customer import Customer
from domain.users.Address import Address
from domain.catalog.Product import Product
from domain.catalog.Price import Price
from domain.money.Currency import Currency
from domain.money.ExchangeRate import ExchangeRate
from domain.checkout.Cart import Cart
from domain.checkout.Order import Order
from domain.checkout.OrderItem import OrderItem
from domain.catalog.Tax import Tax
from domain.payments.Payment import Payment
from domain.payments.PaymentGateway import PaymentGateway
from domain.checkout.Shipment import Shipment

def demo():
    user = User(id=1, email='a@b.c', role='user')
    policy = PasswordPolicy()
    auth = AuthService()
    session = auth.login(user, 'Str0ng!pass', policy)

    cust = Customer(userId=user.id)
    addr = Address(id=1, customer=cust, city='Vilnius')
    addr.validatePostalCode('01100')
    addr.markAsDefault(cust)

    prod = Product(id=1, name='Phone', category=None)
    eur = Currency(code='EUR', symbol='€', fractionDigits=2)
    price = Price(product=prod, amount=599.0, currency=eur)
    rate = ExchangeRate(baseCode='EUR', quoteCode='USD', rate=1.1)
    usd_price = price.convertTo(eur, rate)  # demo

    cart = Cart(id=1, customer=cust)
    _ = cart.addItem(prod, 1)

    order = Order(id=1, customer=cust)
    tax = Tax(region='LT', rate=0.21, inclusive=False)
    oi = OrderItem(id=1, order=order, product=prod)
    subtotal = oi.subtotal(price, 1, tax)

    order.place([oi])
    payment = Payment(id=1, order=order, amount=subtotal)
    gateway = PaymentGateway(id=1, name='TestPay', configId='cfg')
    payment.capture(gateway)

    shipment = Shipment(id=1, order=order)
    shipment.ship()
    shipment.markDelivered()

    print('OK:', session.userId, order.status, f'{subtotal:.2f}')

if __name__ == '__main__':
    demo()
