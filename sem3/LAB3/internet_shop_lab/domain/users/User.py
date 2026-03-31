from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
User with verification & password change via policy entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class User:
    id: int
    email: str
    role: str

    def verifyEmail(self):
        """Mark email as verified; raise if already verified."""

        if self.role == 'verified':
            from exceptions.EmailAlreadyVerifiedException import EmailAlreadyVerifiedException
            raise EmailAlreadyVerifiedException("Email already verified")
        self.role = 'verified'


    def changePassword(self, new_password: str, policy: 'PasswordPolicy'):
        """Validate and change password via policy."""

        if not policy.validate(new_password):
            from exceptions.InvalidPasswordException import InvalidPasswordException
            raise InvalidPasswordException("Password does not meet policy")
        return True

