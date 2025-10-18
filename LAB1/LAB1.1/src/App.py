import tkinter as tk
from tkinter import filedialog, messagebox

from .RubiksCube import RubiksCube  # если в RubiksCube.py класс действительно RubiksCube
from .MenuFrame import MenuFrame
from .GameFrame import GameFrame


class App(tk.Tk):
    """Главное окно приложения."""
    def __init__(self):
        super().__init__()
        self.title("Rubik's Cube")
        self.geometry("+200+120")
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
