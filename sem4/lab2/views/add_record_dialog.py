from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from models.student_record import StudentRecord


class AddRecordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление записи")
        self.resize(500, 400)

        self.full_name_edit = QLineEdit()
        self.group_edit = QLineEdit()
        self.semester_spins = []

        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.addRow("ФИО:", self.full_name_edit)
        form_layout.addRow("Группа:", self.group_edit)

        semesters_group = QGroupBox("Общественная работа по семестрам")
        semesters_layout = QGridLayout()

        for i in range(10):
            label = QLabel(f"{i + 1} семестр")
            spin = QSpinBox()
            spin.setRange(0, 100000)
            self.semester_spins.append(spin)

            row = i // 2
            col = (i % 2) * 2
            semesters_layout.addWidget(label, row, col)
            semesters_layout.addWidget(spin, row, col + 1)

        semesters_group.setLayout(semesters_layout)

        buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton("Добавить")
        self.cancel_button = QPushButton("Отмена")

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(semesters_group)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.ok_button.clicked.connect(self._on_accept)
        self.cancel_button.clicked.connect(self.reject)

    def _on_accept(self):
        try:
            self.get_record()
            self.accept()
        except Exception as error:
            QMessageBox.critical(self, "Ошибка", str(error))

    def get_record(self) -> StudentRecord:
        social_work = [spin.value() for spin in self.semester_spins]
        return StudentRecord(
            full_name=self.full_name_edit.text(),
            group=self.group_edit.text(),
            social_work=social_work
        )