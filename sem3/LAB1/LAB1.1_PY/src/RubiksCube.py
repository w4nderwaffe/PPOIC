from __future__ import annotations
import json
import random
from copy import deepcopy
from typing import Dict, List

Face = List[List[str]]

class RubiksCube:
    """
    3x3 Кубик Рубика.
    Грани: U(верх), D(низ), L(лево), R(право), F(перед), B(зад).
    Цвета по умолчанию: U=W, D=Y, L=O, R=R, F=G, B=B (как примеры ярлыков).
    """

    def __init__(self, randomize_moves: int | None = None):
        self.size = 3
        # Буквы-цвета для наглядности
        self.colors = {'U': 'W', 'D': 'Y', 'L': 'O', 'R': 'R', 'F': 'G', 'B': 'B'}
        self.faces: Dict[str, Face] = {}
        self.reset_solved()
        if randomize_moves:
            self.randomize(randomize_moves)

    # ---------- базовые состояния ----------
    def reset_solved(self) -> None:
        """Собранное состояние."""
        self.faces = {
            f: [[self.colors[f] for _ in range(self.size)] for _ in range(self.size)]
            for f in ('U', 'D', 'L', 'R', 'F', 'B')
        }

    def randomize(self, moves: int = 20) -> None:
        """Перемешивание случайными ходами."""
        all_faces = ['U', 'D', 'L', 'R', 'F', 'B']
        for _ in range(moves):
            face = random.choice(all_faces)
            clockwise = random.choice([True, False])
            turns = random.choice([1, 2, 3])  # 90/180/270
            self.rotate(face, clockwise=clockwise, turns=turns)

    # ---------- загрузка/сохранение ----------
    def load_from_file(self, path: str) -> None:
        """
        Формат JSON:
        {
          "U": "WWWWWWWWW",
          "D": "YYYYYYYYY",
          "L": "OOOOOOOOO",
          "R": "RRRRRRRRR",
          "F": "GGGGGGGGG",
          "B": "BBBBBBBBB"
        }
        По 9 символов на грань (слева-направо, сверху-вниз).
        """
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for face in ('U', 'D', 'L', 'R', 'F', 'B'):
            s = data.get(face)
            if not isinstance(s, str) or len(s) != 9:
                raise ValueError(f"Неверные данные для грани {face}: ожидается 9 символов.")
            # Заполняем 3x3
            grid = [[None] * self.size for _ in range(self.size)]
            k = 0
            for r in range(self.size):
                for c in range(self.size):
                    grid[r][c] = s[k]
                    k += 1
            self.faces[face] = grid

    def save_to_file(self, path: str) -> None:
        """Не требовалось, но полезно для отладки — сохранить текущее состояние."""
        out = {}
        for face in ('U', 'D', 'L', 'R', 'F', 'B'):
            s = "".join(self.faces[face][r][c] for r in range(3) for c in range(3))
            out[face] = s
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

    # ---------- повороты ----------
    def rotate(self, face: str, clockwise: bool = True, turns: int = 1) -> None:
        """Повернуть грань face ('U','D','L','R','F','B') на 90° * turns."""
        if face not in ('U', 'D', 'L', 'R', 'F', 'B'):
            raise ValueError("Легальные грани: U,D,L,R,F,B")
        turns = turns % 4
        for _ in range(turns):
            self._rotate_90(face, clockwise)

    def _rotate_90(self, face: str, clockwise: bool) -> None:
        self._rotate_face_matrix(face, clockwise)
        # Сдвиг ребер вокруг грани. Мэппинг корректный для 3x3.
        seq = []
        if face == 'U':
            seq = [('B','row',0,True), ('R','row',0,False), ('F','row',0,False), ('L','row',0,True)]
        elif face == 'D':
            seq = [('F','row',2,False), ('R','row',2,False), ('B','row',2,True), ('L','row',2,True)]
        elif face == 'F':
            seq = [('U','row',2,False), ('R','col',0,False), ('D','row',0,True), ('L','col',2,True)]
        elif face == 'B':
            seq = [('U','row',0,True), ('L','col',0,False), ('D','row',2,False), ('R','col',2,True)]
        elif face == 'L':
            seq = [('U','col',0,False), ('F','col',0,False), ('D','col',0,False), ('B','col',2,True)]
        elif face == 'R':
            seq = [('U','col',2,False), ('B','col',0,True), ('D','col',2,False), ('F','col',2,False)]

        strips = []
        for f,t,i,rev in seq:
            arr = self._get_row(f,i) if t=='row' else self._get_col(f,i)
            if rev: arr = list(reversed(arr))
            strips.append(arr)

        shifted = [strips[-1]] + strips[:-1] if clockwise else strips[1:] + [strips[0]]

        for (f,t,i,rev), arr in zip(seq, shifted):
            if rev: arr = list(reversed(arr))
            if t == 'row':
                self._set_row(f,i,arr)
            else:
                self._set_col(f,i,arr)

    def _rotate_face_matrix(self, face: str, clockwise: bool) -> None:
        m = self.faces[face]
        n = self.size
        res = [[None]*n for _ in range(n)]
        if clockwise:
            for r in range(n):
                for c in range(n):
                    res[c][n-1-r] = m[r][c]
        else:
            for r in range(n):
                for c in range(n):
                    res[n-1-c][r] = m[r][c]
        self.faces[face] = res

    def _get_row(self, face: str, r: int): return self.faces[face][r][:]
    def _set_row(self, face: str, r: int, vals: List[str]): self.faces[face][r] = vals[:]
    def _get_col(self, face: str, c: int): return [self.faces[face][r][c] for r in range(self.size)]
    def _set_col(self, face: str, c: int, vals: List[str]):
        for r in range(self.size):
            self.faces[face][r][c] = vals[r]

    # ---------- проверки ----------
    def is_solved(self) -> bool:
        """Все 9 стикеров каждой грани одинакового цвета."""
        for face in ('U', 'D', 'L', 'R', 'F', 'B'):
            center = self.faces[face][1][1]
            for r in range(3):
                for c in range(3):
                    if self.faces[face][r][c] != center:
                        return False
        return True

    # ---------- утилиты ----------
    def __str__(self) -> str:
        """Компактная печать состояний граней построчно."""
        def flat(f): return "".join(self.faces[f][r][c] for r in range(3) for c in range(3))
        return "U=" + flat('U') + " D=" + flat('D') + " L=" + flat('L') + \
               " R=" + flat('R') + " F=" + flat('F') + " B=" + flat('B')

    def snapshot(self) -> Dict[str, Face]:
        return deepcopy(self.faces)
