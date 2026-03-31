from __future__ import annotations
from dataclasses import dataclass

"""
OrderItem entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class OrderItem:
    id: int
    order: "Order"
    product: "Product"

    def subtotal(self, price: "Price", qty: int, tax: "Tax"):
        """
        Возвращает сумму по позиции с налогом, если налог не включён.
        Тест ожидает формулу: price.amount * qty * (1 + tax.rate) при tax.inclusive == False.
        """
        base = price.amount * max(1, qty)
        if getattr(tax, "inclusive", False):
            return base
        return base * (1 + tax.rate)