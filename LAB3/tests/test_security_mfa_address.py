import pytest
from exceptions.PIIDataDetectedException import PIIDataDetectedException
from domain.security.MFAChallenge import MFAChallenge
from domain.users.Address import Address
from domain.users.Customer import Customer
from exceptions.AddressValidationException import AddressValidationException

def test_mfa_verify_and_issue():
    mfa = MFAChallenge(id=1, userId=1, type='sms')
    assert mfa.issue() is True
    assert mfa.verify("123456") is True
    with pytest.raises(PIIDataDetectedException):
        mfa.verify("codeABC")

def test_address_validate_and_default():
    addr = Address(id=1, customer=None, city="Vilnius")
    with pytest.raises(AddressValidationException):
        addr.validatePostalCode("12")
    assert addr.validatePostalCode("01100") is True
    c = Customer(userId=1)
    assert addr.markAsDefault(c) is True
    assert c.defaultAddress is addr
