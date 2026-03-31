from PyQt5.QtWidgets import QFileDialog, QMessageBox

from models.paginator import Paginator
from services.repository import RecordRepository
from services.xml_service import XmlService


class MainController:
    def __init__(self, view, add_dialog_class=None, search_dialog_class=None, delete_dialog_class=None):
        self.view = view
        self.repository = RecordRepository()
        self.xml_service = XmlService()
        self.paginator = Paginator([], page_size=self.view.get_page_size(), current_page=1)

        self.add_dialog_class = add_dialog_class
        self.search_dialog_class = search_dialog_class
        self.delete_dialog_class = delete_dialog_class

        self._connect_signals()
        self.refresh_main_table()

    def _connect_signals(self):
        self.view.add_action.triggered.connect(self.open_add_dialog)
        self.view.search_action.triggered.connect(self.open_search_dialog)
        self.view.delete_action.triggered.connect(self.open_delete_dialog)
        self.view.open_action.triggered.connect(self.load_from_file)
        self.view.save_action.triggered.connect(self.save_to_file)
        self.view.exit_action.triggered.connect(self.view.close)

        self.view.first_button.clicked.connect(self.go_to_first_page)
        self.view.prev_button.clicked.connect(self.go_to_previous_page)
        self.view.next_button.clicked.connect(self.go_to_next_page)
        self.view.last_button.clicked.connect(self.go_to_last_page)
        self.view.page_size_spin.valueChanged.connect(self.change_page_size)

    def refresh_main_table(self):
        all_records = self.repository.get_all()
        self.paginator.items = all_records

        if self.paginator.current_page > self.paginator.total_pages:
            self.paginator.current_page = self.paginator.total_pages

        page_items = self.paginator.get_page_items()

        self.view.show_records(
            page_items,
            self.paginator.current_page,
            self.paginator.total_pages,
            self.paginator.total_items
        )

    def add_record(self, record):
        self.repository.add(record)
        self.refresh_main_table()

    def open_add_dialog(self):
        if self.add_dialog_class is None:
            QMessageBox.information(self.view, "Информация", "Диалог добавления пока не подключен.")
            return

        dialog = self.add_dialog_class(self.view)
        if dialog.exec_():
            record = dialog.get_record()
            self.add_record(record)

    def open_search_dialog(self):
        if self.search_dialog_class is None:
            QMessageBox.information(self.view, "Информация", "Диалог поиска пока не подключен.")
            return

        dialog = self.search_dialog_class(self.view, self.repository)
        dialog.exec_()

    def open_delete_dialog(self):
        if self.delete_dialog_class is None:
            QMessageBox.information(self.view, "Информация", "Диалог удаления пока не подключен.")
            return

        dialog = self.delete_dialog_class(self.view, self.repository)
        result = dialog.exec_()

        if result:
            deleted_count = dialog.perform_delete()
            if deleted_count > 0:
                QMessageBox.information(
                    self.view,
                    "Удаление",
                    f"Удалено записей: {deleted_count}"
                )
            else:
                QMessageBox.information(
                    self.view,
                    "Удаление",
                    "Подходящих записей не найдено."
                )
            self.refresh_main_table()

    def save_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self.view,
            "Сохранить XML",
            "",
            "XML Files (*.xml)"
        )

        if not file_path:
            return

        if not file_path.lower().endswith(".xml"):
            file_path += ".xml"

        try:
            self.xml_service.save(self.repository.get_all(), file_path)
            QMessageBox.information(self.view, "Сохранение", "Файл успешно сохранён.")
        except Exception as error:
            QMessageBox.critical(self.view, "Ошибка", str(error))

    def load_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Открыть XML",
            "",
            "XML Files (*.xml)"
        )

        if not file_path:
            return

        try:
            records = self.xml_service.load(file_path)
            self.repository.clear()
            self.repository.extend(records)
            self.paginator.current_page = 1
            self.refresh_main_table()
            QMessageBox.information(self.view, "Загрузка", "Файл успешно загружен.")
        except Exception as error:
            QMessageBox.critical(self.view, "Ошибка", str(error))

    def go_to_first_page(self):
        self.paginator.first_page()
        self.refresh_main_table()

    def go_to_previous_page(self):
        self.paginator.previous_page()
        self.refresh_main_table()

    def go_to_next_page(self):
        self.paginator.next_page()
        self.refresh_main_table()

    def go_to_last_page(self):
        self.paginator.last_page()
        self.refresh_main_table()

    def change_page_size(self, value):
        self.paginator.set_page_size(value)
        self.paginator.current_page = 1
        self.refresh_main_table()