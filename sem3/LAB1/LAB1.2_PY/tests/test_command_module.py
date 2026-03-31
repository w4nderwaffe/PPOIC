from src.Command import Command


def test_command_init_and_repr():
    cmd = Command(symbol="1", move="R", next_state=None)
    assert cmd.symbol == "1"
    assert cmd.move == "R"
    assert cmd.next_state is None
    r = repr(cmd)
    assert "HALT" in r
