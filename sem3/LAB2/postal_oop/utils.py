from __future__ import annotations
from datetime import datetime
import uuid
import hashlib

def now() -> datetime:
    """UTC-время для отметок (трекинг, штемпели, касса)."""
    return datetime.utcnow()

def make_id(prefix: str) -> str:
    """Короткий ID с префиксом: prefix_xxxxxxxxxxxx."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def hash_text(text: str) -> str:
    """Хеш для чеков/контрольных сумм и служебных нужд."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
