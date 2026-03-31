class PaymentDeclinedError(Exception):
    """Платёж отклонён (касса/терминал/наложенный платёж)."""
    pass
