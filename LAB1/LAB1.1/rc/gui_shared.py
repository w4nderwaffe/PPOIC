import os

# Константы/настройки GUI
SAVE_DIR = "/Users/w4nderwaffe/uchebka/PPOIC/LAB1/LAB1.1_PY"
SAVE_PATH = os.path.join(SAVE_DIR, "cube_state.json")

LETTER_TO_HEX = {
    'W': '#FFFFFF',
    'Y': '#FFD500',
    'O': '#FF6F00',
    'R': '#CC0000',
    'G': '#009E60',
    'B': '#0046AD',
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


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)
