from __future__ import annotations
from dataclasses import dataclass

"""
MFAChallenge entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class MFAChallenge:
    id: int
    userId: int
    type: str = "sms"

    def issue(self):
        """Issue MFA code (no-op)."""
        return True

    def verify(self, code: str):
        """
        Verify code; raise PII exception if code contains letters (демо-эвристика).
        """
        if any(ch.isalpha() for ch in code):
            from exceptions.PIIDataDetectedException import PIIDataDetectedException
            raise PIIDataDetectedException("Code contains PII-like data")
        return True