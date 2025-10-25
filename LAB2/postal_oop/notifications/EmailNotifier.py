from __future__ import annotations
from dataclasses import dataclass
from postal_oop.utils import make_id

@dataclass
class EmailNotifier:
    from_addr: str = "noreply@post.local"

    def send_status_update(self, email: str, tracking_id: str, status: str) -> str:
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Некорректный e-mail")
        return make_id("MAIL")
