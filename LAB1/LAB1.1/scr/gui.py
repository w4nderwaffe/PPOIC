import os
import tkinter as tk
from tkinter import filedialog, messagebox
from cube import RubiksCube

# ---------- Константы ----------
SAVE_DIR = "/Users/w4nderwaffe/uchebka/PPOIC/LAB1/LAB1.1_PY"
SAVE_PATH = os.path.join(SAVE_DIR, "cube_state.json")

LETTER_TO_HEX = {
    'W': '#FFFFFF',  # white
    'Y': '#FFD500',  # yellow
    'O': '#FF6F00',  # orange
    'R': '#CC0000',  # red
    'G': '#009E60',  # green
    'B': '#0046AD',  # blue
}

FACE_POS = {
    'U': (0, 1),
    'L': (1, 0),
    'F': (1, 1),
    'R': (1, 2),
    'B': (1, 3),
    'D': (2, 1),
}

CELL, GAP, PAD = 44, 2, 10


# ---------- Утилиты ----------
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


# ---------- Экран меню ----------
class MenuFrame(tk.Frame):
    def __init__(self, master, on_start_solved, on_start_random, on_load_file, on_exit):
        super().__init__(master, bg="#222222")
        self.on_start_solved = on_start_solved
        self.on_start_random = on_start_random
        self.on_load_file = on_load_file
        self.on_exit = on_exit

        title = tk.Label(self, text="Rubik's Cube", fg="#FFFFFF", bg="#222222", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        btn1 = tk.Button(self, text="Начать со собранного", width=30, command=self.on_start_solved)
        btn2 = tk.Button(self, text="Начать со случайного", width=30, command=self.on_start_random)
        btn3 = tk.Button(self, text="Загрузить из файла…", width=30, command=self.on_load_file)
        btn4 = tk.Button(self, text="Выйти", width=30, command=self.on_exit)

        for b in (btn1, btn2, btn3, btn4):
            b.pack(pady=6)


# ---------- Экран игры ----------
class GameFrame(tk.Frame):
    def __init__(self, master, cube: RubiksCube, on_back_to_menu):
        super().__init__(master, bg="#1f1f1f")
        self.cube = cube
        self.on_back_to_menu = on_back_to_menu
        self.last_move = ('U', True, 1)

        # Холст
        width = PAD*2 + (4*3)*CELL + (4*3-1)*GAP
        height = PAD*2 + (3*3)*CELL + (3*3-1)*GAP
        self.canvas = tk.Canvas(self, width=width, height=height, bg="#222222", highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=6, padx=8, pady=8)

        # Кнопки ходов
        moves = [
            ('U', lambda: self.turn('U', True, 1)), ("U'", lambda: self.turn('U', False, 1)), ('U2', lambda: self.turn('U', True, 2)),
            ('D', lambda: self.turn('D', True, 1)), ("D'", lambda: self.turn('D', False, 1)), ('D2', lambda: self.turn('D', True, 2)),
            ('L', lambda: self.turn('L', True, 1)), ("L'", lambda: self.turn('L', False, 1)), ('L2', lambda: self.turn('L', True, 2)),
            ('R', lambda: self.turn('R', True, 1)), ("R'", lambda: self.turn('R', False, 1)), ('R2', lambda: self.turn('R', True, 2)),
            ('F', lambda: self.turn('F', True, 1)), ("F'", lambda: self.turn('F', False, 1)), ('F2', lambda: self.turn('F', True, 2)),
            ('B', lambda: self.turn('B', True, 1)), ("B'", lambda: self.turn('B', False, 1)), ('B2', lambda: self.turn('B', True, 2)),
        ]
        for idx, (txt, cmd) in enumerate(moves):
            r = 1 + idx // 6
            c = idx % 6
            tk.Button(self, text=txt, width=5, command=cmd).grid(row=r, column=c, padx=2, pady=2)

        # Нижняя панель: scramble / save / load / reset / back
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
        for key in ['U','D','L','R','F','B']:
            root.bind(key, lambda e, k=key: self.turn(k, True, 1))
            root.bind(key.lower(), lambda e, k=key: self.turn(k, False, 1))  # строчная = против часовой
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
            ensure_dir(SAVE_DIR)
            self.cube.save_to_file(SAVE_PATH)
            messagebox.showinfo("Сохранено", f"Состояние сохранено в:\n{SAVE_PATH}")
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
                    x = PAD + (c_off*3 + c) * (CELL + GAP)
                    y = PAD + (r_off*3 + r) * (CELL + GAP)
                    self.canvas.create_rectangle(x, y, x+CELL, y+CELL, fill=color, outline="#111111", width=1)
        self.solved_var.set(f"Solved: {self.cube.is_solved()}")


# ---------- Приложение ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rubik's Cube")
        self.geometry("+200+120")  # позиция окна
        self.configure(bg="#222222")

        self.menu_frame = MenuFrame(
            self,
            on_start_solved=self.start_solved,
            on_start_random=self.start_random,
            on_load_file=self.start_from_file,
            on_exit=self.quit_app
        )
        self.menu_frame.pack(fill="both", expand=True)

        self.game_frame: GameFrame | None = None

    # --- обработчики меню ---
    def start_solved(self):
        cube = RubiksCube()
        self.show_game(cube)

    def start_random(self):
        cube = RubiksCube(randomize_moves=25)
        self.show_game(cube)

    def start_from_file(self):
        path = filedialog.askopenfilename(
            title="Выбери JSON состояния",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            cube = RubiksCube()
            cube.load_from_file(path)
            self.show_game(cube)
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", str(e))

    def quit_app(self):
        self.destroy()

    # --- показ экранов ---
    def show_menu(self):
        if self.game_frame:
            self.game_frame.destroy()
            self.game_frame = None
        self.menu_frame.pack(fill="both", expand=True)

    def show_game(self, cube: RubiksCube):
        self.menu_frame.pack_forget()
        if self.game_frame:
            self.game_frame.destroy()
        self.game_frame = GameFrame(self, cube, on_back_to_menu=self.show_menu)
        self.game_frame.pack(fill="both", expand=True)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
