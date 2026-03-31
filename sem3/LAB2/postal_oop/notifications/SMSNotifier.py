from __future__ import annotations
from dataclasses import dataclass
from postal_oop.utils import make_id

@dataclass
class SMSNotifier:
    sender_id: str = "POST"

    def send_status_update(self, phone: str, tracking_id: str, status: str) -> str:
        if not phone or not phone.replace("+", "").isdigit():
            raise ValueError("Некорректный номер телефона")
        # Возвращаем ID отправленного сообщения (эмуляция)
        return make_id("SMS")
