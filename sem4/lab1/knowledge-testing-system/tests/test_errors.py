from src.common.errors import AppError


def test_error_creation():

    err = AppError("error")

    assert str(err) == "error"