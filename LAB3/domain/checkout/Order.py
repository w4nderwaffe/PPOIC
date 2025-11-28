from dataclasses import dataclass
from typing import List

@dataclass
class Order:
    id: int
    customer: "Customer"
    status: str = "NEW"

    def place(self, items: list):
        """
        Оформляет заказ, создавая OrderItem объекты.
        Это и есть ассоциация Order → OrderItem.
        """
        from domain.checkout.OrderItem import OrderItem

        created_items = []
        for idx, product in enumerate(items, start=1):
            created_items.append(OrderItem(
                id=idx,
                order=self,
                product=product
            ))

        self.status = "PLACED"
        return created_items
