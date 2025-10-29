import pytest
from domain.catalog.Product import Product
from domain.catalog.Category import Category
from domain.catalog.Brand import Brand
from domain.catalog.InventoryItem import InventoryItem
from domain.catalog.Price import Price
from domain.catalog.Tax import Tax
from domain.money.Currency import Currency
from domain.money.ExchangeRate import ExchangeRate
from domain.checkout.Cart import Cart
from domain.checkout.Order import Order
from domain.checkout.OrderItem import OrderItem
from domain.checkout.Shipment import Shipment
from domain.checkout.DeliveryMethod import DeliveryMethod
from exceptions.InsufficientInventoryException import InsufficientInventoryException
from exceptions.OrderAlreadyShippedException import OrderAlreadyShippedException

def test_catalog_and_pricing_and_tax():
    cat = Category(id=1, name="Phones", parent=None)
    prod = Product(id=1, name="Phone", category=cat)
    prod.rename("Super Phone")
    prod.changeSku("SKU123")
    assert "SKU=SKU123" in prod.name

    brand = Brand(id=1, name="Acme", country="LT")
    assert brand.verifyBrand() is True
    brand.rename("Acme Inc.")
    assert brand.name == "Acme Inc."

    eur = Currency(code="EUR", symbol="€", fractionDigits=2)
    price = Price(product=prod, amount=100.0, currency=eur)
    rate = ExchangeRate(baseCode="EUR", quoteCode="USD", rate=1.1)
    conv = price.convertTo(eur, rate)
    assert conv.amount == pytest.approx(110.0)

    tax = Tax(region="LT", rate=0.21, inclusive=False)
    assert tax.compute(100.0) == pytest.approx(21.0)
    incl = tax.toggleInclusive()
    assert incl is True

def test_cart_order_checkout_flow():
    eur = Currency(code="EUR", symbol="€", fractionDigits=2)
    prod = Product(id=2, name="Headphones", category=None)
    price = Price(product=prod, amount=50.0, currency=eur)
    tax = Tax(region="LT", rate=0.21, inclusive=False)

    from domain.users.Customer import Customer
    c = Customer(userId=1)
    cart = Cart(id=1, customer=c)
    item = cart.addItem(prod, 2)
    assert item.cart.id == cart.id

    order = Order(id=10, customer=c)
    oi = OrderItem(id=1, order=order, product=prod)
    st = oi.subtotal(price, 2, tax)
    assert st == pytest.approx(50.0*2*(1+0.21))

    order.place([oi])
    ship = Shipment(id=1, order=order)
    ship.ship()
    with pytest.raises(OrderAlreadyShippedException):
        order.cancel()
    ship.markDelivered()
    assert order.status == "DELIVERED"

def test_inventory_and_delivery():
    prod = Product(id=3, name="Mouse", category=None)
    inv = InventoryItem(id=1, product=prod, quantity=1)
    inv.increaseStock(4)
    assert inv.quantity == 5
    with pytest.raises(InsufficientInventoryException):
        inv.decreaseStock(10)
    assert inv.decreaseStock(2) == 3

    from domain.users.Address import Address
    from domain.users.Customer import Customer
    addr = Address(id=1, customer=Customer(userId=2), city="Vilnius")
    dm = DeliveryMethod(id=1, name="Post", basePrice=3.0)
    assert dm.isAvailableForAddress(addr) is True
    assert dm.quote(addr) == 3.0
