from .App import App
from .MenuFrame import MenuFrame
from .GameFrame import GameFrame

# Эти объекты тесты патчат через src.gui.*
from .gui_shared import SAVE_DIR, SAVE_PATH
from tkinter import filedialog, messagebox

__all__ = [
    "App",
    "MenuFrame",
    "GameFrame",
    "SAVE_DIR",
    "SAVE_PATH",
    "filedialog",
    "messagebox",
]
