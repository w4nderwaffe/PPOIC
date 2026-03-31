from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAction,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа 2 — Вариант 2")
        self.resize(1400, 700)

        self.add_action = QAction("Добавить", self)
        self.search_action = QAction("Поиск", self)
        self.delete_action = QAction("Удаление", self)
        self.open_action = QAction("Открыть", self)
        self.save_action = QAction("Сохранить", self)
        self.exit_action = QAction("Выход", self)

        self._create_menu()
        self._create_toolbar()
        self._create_ui()

    def _create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        records_menu = menu_bar.addMenu("Записи")
        records_menu.addAction(self.add_action)
        records_menu.addAction(self.search_action)
        records_menu.addAction(self.delete_action)

    def _create_toolbar(self):
        toolbar = QToolBar("Основная панель")
        self.addToolBar(toolbar)

        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.add_action)
        toolbar.addAction(self.search_action)
        toolbar.addAction(self.delete_action)

    def _create_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        self.table = QTableWidget()
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

        self.first_button = QPushButton("<<")
        self.prev_button = QPushButton("<")
        self.next_button = QPushButton(">")
        self.last_button = QPushButton(">>")

        self.page_size_label = QLabel("Записей на странице:")
        self.page_size_spin = QSpinBox()
        self.page_size_spin.setRange(1, 100)
        self.page_size_spin.setValue(10)

        self.page_info_label = QLabel("Страница 1 из 1")
        self.total_info_label = QLabel("Всего записей: 0")

        pagination_layout.addWidget(self.first_button)
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.next_button)
        pagination_layout.addWidget(self.last_button)
        pagination_layout.addSpacing(20)
        pagination_layout.addWidget(self.page_size_label)
        pagination_layout.addWidget(self.page_size_spin)
        pagination_layout.addSpacing(20)
        pagination_layout.addWidget(self.page_info_label)
        pagination_layout.addSpacing(20)
        pagination_layout.addWidget(self.total_info_label)
        pagination_layout.addStretch()

        main_layout.addWidget(self.table)
        main_layout.addLayout(pagination_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_records(self, records, current_page: int, total_pages: int, total_items: int):
        self.table.setRowCount(len(records))

        for row, record in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(record.full_name))
            self.table.setItem(row, 1, QTableWidgetItem(record.group))

            for index, value in enumerate(record.social_work):
                self.table.setItem(row, index + 2, QTableWidgetItem(str(value)))

            self.table.setItem(row, 12, QTableWidgetItem(str(record.total_social_work)))

        self.page_info_label.setText(f"Страница {current_page} из {total_pages}")
        self.total_info_label.setText(f"Всего записей: {total_items}")

    def get_page_size(self) -> int:
        return self.page_size_spin.value()