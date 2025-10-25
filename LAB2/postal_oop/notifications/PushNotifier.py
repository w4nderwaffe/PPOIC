from __future__ import annotations
from dataclasses import dataclass
from postal_oop.utils import make_id

@dataclass
class PushNotifier:
    provider: str = "local"

    def send_status_update(self, device_token: str, tracking_id: str, status: str) -> str:
        if not device_token or len(device_token) < 8:
            raise ValueError("Некорректный device_token")
        # Эмуляция отправки: возвращаем ID пуш-сообщения
        return make_id("PUSH")
