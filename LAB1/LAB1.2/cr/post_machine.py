# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import List


class PostMachine:

    def __init__(self, tape_size: int = 20):
        if tape_size <= 0:
            raise ValueError("Размер ленты должен быть положительным.")
        self.tape: List[int] = [0] * tape_size
        self.head: int = tape_size // 2

    def set_tape(self, state: str) -> None:
        tape: List[int] = []
        for ch in state:
            if ch == "0" or ch == "1":
                tape.append(0 if ch == "0" else 1)
        self.tape = tape
        self.head = len(self.tape) // 2 if self.tape else 0  # как в C++: середина актуального массива

    def execute(self, command: str) -> None:
        cmd = command.strip()
        if cmd == "LEFT":
            if self.head > 0:
                self.head -= 1
            self.print_tape()
        elif cmd == "RIGHT":
            if self.head < len(self.tape) - 1:
                self.head += 1
            self.print_tape()
        elif cmd == "MARK":
            if not self.tape:
                self.tape = [0]
                self.head = 0
            self.tape[self.head] = 1
            self.print_tape()
        elif cmd == "ERASE":
            if not self.tape:
                self.tape = [0]
                self.head = 0
            self.tape[self.head] = 0
            self.print_tape()
        elif cmd == "STOP":
            print("Остановка машины.")
            raise SystemExit(0)
        else:
            print(f"Неизвестная команда: {command}")
            return

    def print_tape(self) -> None:
        out_parts = []
        for i, val in enumerate(self.tape):
            if i == self.head:
                out_parts.append(f"[{val}]")
            else:
                out_parts.append(f" {val} ")
        print("".join(out_parts))


def main() -> None:
    import sys
    machine = PostMachine(20)

    print("Введите начальное состояние ленты (например 0001000): ", end="")
    try:
        state = input().strip()
    except EOFError:
        state = ""
    machine.set_tape(state)

    print("Машина Поста готова. Доступные команды: LEFT, RIGHT, MARK, ERASE, STOP")

    while True:
        try:
            cmd = input("> ").strip()
        except EOFError:
            break
        if not cmd:
            continue
        try:
            machine.execute(cmd)
        except SystemExit as e:
            sys.exit(e.code)


if __name__ == "__main__":
    main()
