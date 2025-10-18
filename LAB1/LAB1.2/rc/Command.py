from dataclasses import dataclass
from typing import Optional


@dataclass
class Command:
    symbol: str
    move: str
    next_state: Optional[int]

    def __repr__(self) -> str:
        nxt = self.next_state if self.next_state is not None else "HALT"
        return f"Command(symbol={self.symbol!r}, move={self.move!r}, next_state={nxt})"
