from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from models.criteria import SearchCriteria
from models.paginator import Paginator


class SearchDialog(QDialog):
    def __init__(self, parent=None, repository=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск записей")
        self.resize(1400, 700)

        self.repository = repository
        self.search_results = []
        self.paginator = Paginator([], page_size=10, current_page=1)

        self.surname_edit = QLineEdit()
        self.group_combo = QComboBox()
        self.min_spin = QSpinBox()
        self.max_spin = QSpinBox()

        self.search_button = QPushButton("Найти")
        self.close_button = QPushButton("Закрыть")

        self.table = QTableWidget()

        self.first_button = QPushButton("<<")
        self.prev_button = QPushButton("<")
        self.next_button = QPushButton(">")
        self.last_button = QPushButton(">>")
        self.page_size_spin = QSpinBox()
        self.page_info_label = QLabel("Страница 1 из 1")
        self.total_info_label = QLabel("Всего записей: 0")

        self._build_ui()
        self._fill_groups()
        self._connect_signals()

    def _build_ui(self):
        main_layout = QVBoxLayout()

        criteria_group = QGroupBox("Условия поиска")
        criteria_layout = QGridLayout()

        self.group_combo.addItem("Не выбрано", "")
        self.min_spin.setRange(0, 100000)
        self.max_spin.setRange(0, 100000)
        self.max_spin.setValue(100000)
        self.page_size_spin.setRange(1, 100)
        self.page_size_spin.setValue(10)

        criteria_layout.addWidget(QLabel("Фамилия:"), 0, 0)
        criteria_layout.addWidget(self.surname_edit, 0, 1)
        criteria_layout.addWidget(QLabel("Группа:"), 0, 2)
        criteria_layout.addWidget(self.group_combo, 0, 3)
        criteria_layout.addWidget(QLabel("Мин. количество:"), 1, 0)
        criteria_layout.addWidget(self.min_spin, 1, 1)
        criteria_layout.addWidget(QLabel("Макс. количество:"), 1, 2)
        criteria_layout.addWidget(self.max_spin, 1, 3)

        criteria_group.setLayout(criteria_layout)

        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels([
            "ФИО",
            "Группа",
            "1 сем.",
            "2 сем.",
            "3 сем.",
            "4 сем.",
            "5 сем.",
            "6 сем.",
            "7 сем.",
            "8 сем.",
            "9 сем.",
            "10 сем.",
            "Сумма"
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)

        pagination_layout = QHBoxLayout()
        pagination_layout.addWidget(self.first_button)
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.next_button)
        pagination_layout.addWidget(self.last_button)
        pagination_layout.addSpacing(20)
        pagination_layout.addWidget(QLabel("Записей на странице:"))
        pagination_layout.addWidget(self.page_size_spin)
        pagination_layout.addSpacing(20)
        pagination_layout.addWidget(self.page_info_label)
        pagination_layout.addSpacing(20)
        pagination_layout.addWidget(self.total_info_label)
        pagination_layout.addStretch()

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.search_button)
        buttons_layout.addWidget(self.close_button)

        main_layout.addWidget(criteria_group)
        main_layout.addWidget(self.table)
        main_layout.addLayout(pagination_layout)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def _fill_groups(self):
        if self.repository is None:
            return

        for group in self.repository.get_groups():
            self.group_combo.addItem(group, group)

    def _connect_signals(self):
        self.search_button.clicked.connect(self.perform_search)
        self.close_button.clicked.connect(self.reject)

        self.first_button.clicked.connect(self.go_to_first_page)
        self.prev_button.clicked.connect(self.go_to_previous_page)
        self.next_button.clicked.connect(self.go_to_next_page)
        self.last_button.clicked.connect(self.go_to_last_page)
        self.page_size_spin.valueChanged.connect(self.change_page_size)

    def _build_criteria(self) -> SearchCriteria:
        surname = self.surname_edit.text().strip() or None
        group = self.group_combo.currentData() or None

        min_total = self.min_spin.value()
        max_total = self.max_spin.value()

        use_range = not (min_total == 0 and max_total == 100000)

        return SearchCriteria(
            surname=surname,
            group=group,
            min_total=min_total if use_range else None,
            max_total=max_total if use_range else None
        )

    def perform_search(self):
        if self.repository is None:
            return

        criteria = self._build_criteria()
        self.search_results = self.repository.search(criteria)

        self.paginator.items = self.search_results
        self.paginator.current_page = 1
        self.paginator.set_page_size(self.page_size_spin.value())

        self._refresh_table()

    def _refresh_table(self):
        page_items = self.paginator.get_page_items()
        self.table.setRowCount(len(page_items))

        for row, record in enumerate(page_items):
            self.table.setItem(row, 0, QTableWidgetItem(record.full_name))
            self.table.setItem(row, 1, QTableWidgetItem(record.group))

            for index, value in enumerate(record.social_work):
                self.table.setItem(row, index + 2, QTableWidgetItem(str(value)))

            self.table.setItem(row, 12, QTableWidgetItem(str(record.total_social_work)))

        self.page_info_label.setText(
            f"Страница {self.paginator.current_page} из {self.paginator.total_pages}"
        )
        self.total_info_label.setText(f"Всего записей: {self.paginator.total_items}")

    def go_to_first_page(self):
        self.paginator.first_page()
        self._refresh_table()

    def go_to_previous_page(self):
        self.paginator.previous_page()
        self._refresh_table()

    def go_to_next_page(self):
        self.paginator.next_page()
        self._refresh_table()

    def go_to_last_page(self):
        self.paginator.last_page()
        self._refresh_table()

    def change_page_size(self, value):
        self.paginator.set_page_size(value)
        self.paginator.current_page = 1
        self._refresh_table()