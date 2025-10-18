import os
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable, Tuple

from .RubiksCube import RubiksCube
from .gui_shared import (
    LETTER_TO_HEX,
    FACE_POS,
    CELL,
    GAP,
    PAD,
    ensure_dir,
)


class GameFrame(tk.Frame):
    """Экран игры."""
    def __init__(self, master, cube: RubiksCube, on_back_to_menu: Callable[[], None]):
        super().__init__(master, bg="#1f1f1f")
        self.cube = cube
        self.on_back_to_menu = on_back_to_menu
        self.last_move: Tuple[str, bool, int] = ('U', True, 1)

        # Холст
        width = PAD * 2 + (4 * 3) * CELL + (4 * 3 - 1) * GAP
        height = PAD * 2 + (3 * 3) * CELL + (3 * 3 - 1) * GAP
        self.canvas = tk.Canvas(
            self, width=width, height=height, bg="#222222", highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, columnspan=6, padx=8, pady=8)

        # Кнопки ходов
        moves = [
            ('U', lambda: self.turn('U', True, 1)),  ("U'", lambda: self.turn('U', False, 1)), ('U2', lambda: self.turn('U', True, 2)),
            ('D', lambda: self.turn('D', True, 1)),  ("D'", lambda: self.turn('D', False, 1)), ('D2', lambda: self.turn('D', True, 2)),
            ('L', lambda: self.turn('L', True, 1)),  ("L'", lambda: self.turn('L', False, 1)), ('L2', lambda: self.turn('L', True, 2)),
            ('R', lambda: self.turn('R', True, 1)),  ("R'", lambda: self.turn('R', False, 1)), ('R2', lambda: self.turn('R', True, 2)),
            ('F', lambda: self.turn('F', True, 1)),  ("F'", lambda: self.turn('F', False, 1)), ('F2', lambda: self.turn('F', True, 2)),
            ('B', lambda: self.turn('B', True, 1)),  ("B'", lambda: self.turn('B', False, 1)), ('B2', lambda: self.turn('B', True, 2)),
        ]
        for idx, (txt, cmd) in enumerate(moves):
            r = 1 + idx // 6
            c = idx % 6
            tk.Button(self, text=txt, width=5, command=cmd).grid(row=r, column=c, padx=2, pady=2)

        # Нижняя панель
        tk.Button(self, text="Scramble 25", command=lambda: self.scramble(25)).grid(row=4, column=0, padx=2, pady=6, sticky="ew")
        tk.Button(self, text="Reset", command=self.reset).grid(row=4, column=1, padx=2, pady=6, sticky="ew")
        tk.Button(self, text="Load…", command=self.load_from_file_dialog).grid(row=4, column=2, padx=2, pady=6, sticky="ew")
        tk.Button(self, text="Save", command=self.save_to_fixed_path).grid(row=4, column=3, padx=2, pady=6, sticky="ew")
        tk.Button(self, text="Выйти в меню", command=self.on_back_to_menu).grid(row=4, column=4, columnspan=2, padx=2, pady=6, sticky="nsew")

        self.solved_var = tk.StringVar()
        self.solved_lbl = tk.Label(self, textvariable=self.solved_var, fg="#DDDDDD", bg="#333333")
        self.solved_lbl.grid(row=5, column=0, columnspan=6, sticky="nsew", padx=8, pady=4)

        # Горячие клавиши
        self.bind_all_keys()
        self.redraw()

    # --- привязки клавиш ---
    def bind_all_keys(self):
        root = self.winfo_toplevel()
        for key in ['U', 'D', 'L', 'R', 'F', 'B']:
            root.bind(key,        lambda e, k=key: self.turn(k, True, 1))
            root.bind(key.lower(), lambda e, k=key: self.turn(k, False, 1))
        root.bind('2', self.double_last_move)

    # --- действия ---
    def turn(self, face, clockwise=True, turns=1):
        self.cube.rotate(face, clockwise=clockwise, turns=turns)
        self.last_move = (face, clockwise, turns)
        self.redraw()

    def double_last_move(self, _=None):
        face, clockwise, _t = self.last_move
        self.turn(face, clockwise, 2)

    def scramble(self, n=25):
        self.cube.randomize(n)
        self.redraw()

    def reset(self):
        self.cube.reset_solved()
        self.redraw()

    def load_from_file_dialog(self):
        initial_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        path = filedialog.askopenfilename(
            title="Загрузить состояние (JSON)",
            initialdir=os.path.abspath(initial_dir),
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            self.cube.load_from_file(path)
            self.redraw()
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", str(e))

    def save_to_fixed_path(self):
        try:
            # Берём актуальные (в т.ч. запатченные тестами) пути из фасада src.gui
            from . import gui as _gui
            ensure_dir(_gui.SAVE_DIR)
            self.cube.save_to_file(_gui.SAVE_PATH)
            messagebox.showinfo("Сохранено", f"Состояние сохранено в:\n{_gui.SAVE_PATH}")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))

    # --- отрисовка ---
    def redraw(self):
        self.canvas.delete("all")
        for face, (r_off, c_off) in FACE_POS.items():
            for r in range(3):
                for c in range(3):
                    letter = self.cube.faces[face][r][c]
                    color = LETTER_TO_HEX.get(letter, "#888888")
                    x = PAD + (c_off * 3 + c) * (CELL + GAP)
                    y = PAD + (r_off * 3 + r) * (CELL + GAP)
                    self.canvas.create_rectangle(
                        x, y, x + CELL, y + CELL, fill=color, outline="#111111", width=1
                    )
        self.solved_var.set(f"Solved: {self.cube.is_solved()}")
