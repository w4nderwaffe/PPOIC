from typing import List, Optional


class PostMachine:
    def __init__(self, size: int = 20):
        if size <= 0:
            raise ValueError("Size must be positive")
        self._size = size
        self._tape: List[int] = [0] * size
        self._head: int = size // 2

    @property
    def size(self) -> int:
        return self._size

    @property
    def head(self) -> int:
        return self._head

    @property
    def tape(self) -> List[int]:
        return self._tape

    def _clamp_head(self) -> None:
        if not self._tape:
            self._head = 0
            return
        if self._head < 0:
            self._head = 0
        elif self._head >= len(self._tape):
            self._head = len(self._tape) - 1

    def _format_tape_with_head(self) -> str:
        if not self._tape:
            return "[]"
        self._clamp_head()
        parts = [str(x) for x in self._tape]
        parts[self._head] = f"[{parts[self._head]}]"
        return "".join(parts)

    def print_tape(self) -> str:
        out = self._format_tape_with_head()
        print(out)
        return out

    def set_tape(self, s: str) -> None:
        filtered = [1 if ch == "1" else 0 for ch in s if ch in ("0", "1")]
        self._tape = filtered
        if self._tape:
            self._head = len(self._tape) // 2
        else:
            self._head = 0

    def execute(self, cmd: str) -> Optional[str]:
        if cmd is None:
            return None
        c = cmd.strip().upper()
        if c == "":
            return None
        if c == "LEFT":
            if self._tape and self._head > 0:
                self._head -= 1
            return self.print_tape()
        if c == "RIGHT":
            if self._tape and self._head < len(self._tape) - 1:
                self._head += 1
            return self.print_tape()
        if c == "MARK":
            if not self._tape:
                self._tape = [1]
                self._head = 0
            else:
                self._tape[self._head] = 1
            return self.print_tape()
        if c == "ERASE":
            if not self._tape:
                self._tape = [0]
                self._head = 0
            else:
                self._tape[self._head] = 0
            return self.print_tape()
        if c == "PRINT":
            return self.print_tape()
        if c == "STOP":
            print("Остановка машины.")
            raise SystemExit(0)
        print(f"Неизвестная команда: {c}")
        return None

    def __repr__(self) -> str:
        return f"PostMachine(size={self._size}, head={self._head}, tape={''.join(str(x) for x in self._tape)})"


def main(argv=None) -> int:
    from .post_machine_main import main as _cli_main
    return _cli_main(argv)
