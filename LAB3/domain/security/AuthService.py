from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

"""
AuthService entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class AuthService:
    lastOtpAt: datetime | None = None
    provider: str = "local"
    attempts: int = 0

    def login(self, user: "User", password: str, policy: "PasswordPolicy"):
        """Check password via policy; create session."""
        self.attempts += 1
        if not policy.validate(password):
            from exceptions.InvalidPasswordException import InvalidPasswordException
            raise InvalidPasswordException("Invalid password")
        from domain.security.Session import Session
        return Session(id=self.attempts, userId=user.id, expiresAt=datetime.utcnow())

    def logout(self, session: "Session"):
        """Invalidate the session."""
        session.invalidate()
        return True