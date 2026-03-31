import pytest
from domain.users.User import User
from domain.security.PasswordPolicy import PasswordPolicy
from domain.security.AuthService import AuthService
from exceptions.EmailAlreadyVerifiedException import EmailAlreadyVerifiedException
from exceptions.InvalidPasswordException import InvalidPasswordException

def test_user_verify_and_change_password():
    u = User(id=1, email="e@x", role="user")
    u.verifyEmail()
    assert u.role == "verified"
    with pytest.raises(EmailAlreadyVerifiedException):
        u.verifyEmail()

    policy = PasswordPolicy(minLength=6, requireSymbol=True)
    assert u.changePassword("A@bcdef", policy) is True
    with pytest.raises(InvalidPasswordException):
        u.changePassword("short", policy)

def test_auth_login_logout_and_policy():
    u = User(id=2, email="a@b", role="user")
    policy = PasswordPolicy(minLength=8, requireSymbol=True)
    auth = AuthService()
    with pytest.raises(InvalidPasswordException):
        auth.login(u, "weakpass", policy)
    ses = auth.login(u, "Str0ng!p", policy)
    assert ses.userId == u.id
    assert ses.refresh() is not None
    assert ses.invalidate() is True
