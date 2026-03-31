import random
import sys

from PyQt5.QtWidgets import QApplication

from controllers.main_controller import MainController
from models.student_record import StudentRecord
from views.add_record_dialog import AddRecordDialog
from views.delete_dialog import DeleteDialog
from views.main_window import MainWindow
from views.search_dialog import SearchDialog


def generate_random_records(count: int = 50) -> list[StudentRecord]:
    surnames = [
        "Иванов",
        "Петров",
        "Сидоров",
        "Козлов",
        "Новиков",
    ]

    names = [
        "Иван",
        "Андрей",
        "Дмитрий",
        "Максим",
        "Алексей",
    ]

    patronymics = [
        "Иванович",
        "Андреевич",
        "Дмитриевич",
        "Максимович",
        "Алексеевич",
    ]

    groups = [
        "321701",
        "421701",
        "421703",
        "421702",
        "221701",
        "221702",
    ]

    records = []

    for _ in range(count):
        full_name = f"{random.choice(surnames)} {random.choice(names)} {random.choice(patronymics)}"
        group = random.choice(groups)
        social_work = [random.randint(0, 10) for _ in range(10)]

        record = StudentRecord(
            full_name=full_name,
            group=group,
            social_work=social_work
        )
        records.append(record)

    return records


def create_app():
    qt_app = QApplication(sys.argv)

    window = MainWindow()

    controller = MainController(
        window,
        add_dialog_class=AddRecordDialog,
        search_dialog_class=SearchDialog,
        delete_dialog_class=DeleteDialog
    )

    controller.repository.extend(generate_random_records(50))
    controller.refresh_main_table()

    window.show()
    window.raise_()
    window.activateWindow()

    qt_app.main_window = window
    qt_app.main_controller = controller

    return qt_app