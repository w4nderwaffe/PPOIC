from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

"""
EmailMessage entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class EmailMessage:
    id: int
    toAddress: str
    subject: str = ""

    def render(self, template: str, context: Dict[str, Any]):
        """Render with template (fake)."""
        return template.format(**context) if context else template

    def dispatch(self):
        """Dispatch email (no-op)."""
        return True