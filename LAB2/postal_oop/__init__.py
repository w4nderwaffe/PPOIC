# Корневой пакет физической почты.
# Здесь только утилиты, чтобы не тянуть под-пакеты преждевременно.
from .utils import now, make_id, hash_text

__all__ = ["now", "make_id", "hash_text"]
