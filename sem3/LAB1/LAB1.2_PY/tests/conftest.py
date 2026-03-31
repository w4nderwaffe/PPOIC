import sys
from pathlib import Path

# Добавляем КОРЕНЬ проекта в sys.path, чтобы работал импорт "from src.xxx import ..."
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
