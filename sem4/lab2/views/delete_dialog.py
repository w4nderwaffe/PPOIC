from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from models.criteria import DeleteCriteria


class DeleteDialog(QDialog):
    def __init__(self, parent=None, repository=None):
        super().__init__(parent)
        self.setWindowTitle("Удаление записей")
        self.resize(500, 250)

        self.repository = repository

        self.surname_edit = QLineEdit()
        self.group_combo = QComboBox()
        self.min_spin = QSpinBox()
        self.max_spin = QSpinBox()

        self.delete_button = QPushButton("Удалить")
        self.cancel_button = QPushButton("Отмена")

        self._build_ui()
        self._fill_groups()

    def _build_ui(self):
        main_layout = QVBoxLayout()

        criteria_group = QGroupBox("Условия удаления")
        criteria_layout = QGridLayout()

        self.group_combo.addItem("Не выбрано", "")
        self.min_spin.setRange(0, 100000)
        self.max_spin.setRange(0, 100000)
        self.max_spin.setValue(100000)

        criteria_layout.addWidget(QLabel("Фамилия:"), 0, 0)
        criteria_layout.addWidget(self.surname_edit, 0, 1)
        criteria_layout.addWidget(QLabel("Группа:"), 0, 2)
        criteria_layout.addWidget(self.group_combo, 0, 3)
        criteria_layout.addWidget(QLabel("Мин. количество:"), 1, 0)
        criteria_layout.addWidget(self.min_spin, 1, 1)
        criteria_layout.addWidget(QLabel("Макс. количество:"), 1, 2)
        criteria_layout.addWidget(self.max_spin, 1, 3)

        criteria_group.setLayout(criteria_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.cancel_button)

        main_layout.addWidget(criteria_group)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.delete_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def _fill_groups(self):
        if self.repository is None:
            return

        for group in self.repository.get_groups():
            self.group_combo.addItem(group, group)

    def _build_criteria(self) -> DeleteCriteria:
        surname = self.surname_edit.text().strip() or None
        group = self.group_combo.currentData() or None

        min_total = self.min_spin.value()
        max_total = self.max_spin.value()

        use_range = not (min_total == 0 and max_total == 100000)

        return DeleteCriteria(
            surname=surname,
            group=group,
            min_total=min_total if use_range else None,
            max_total=max_total if use_range else None
        )

    def perform_delete(self) -> int:
        if self.repository is None:
            return 0

        criteria = self._build_criteria()
        return self.repository.delete(criteria)