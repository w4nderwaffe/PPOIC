from models.student_record import StudentRecord
from services.repository import RecordRepository
from views.add_record_dialog import AddRecordDialog
from views.delete_dialog import DeleteDialog
from views.main_window import MainWindow
from views.search_dialog import SearchDialog


def make_repository():
    repository = RecordRepository()
    repository.extend([
        StudentRecord("Иванов Иван Иванович", "ПИ-21", [1] * 10),
        StudentRecord("Петров Петр Петрович", "ПИ-22", [2] * 10),
        StudentRecord("Сидоров Сидор Сидорович", "ПИ-21", [3] * 10),
    ])
    return repository


def test_main_window_initial_state(qapp):
    window = MainWindow()

    assert window.windowTitle() == "Лабораторная работа 2 — Вариант 2"
    assert window.table.columnCount() == 13
    assert window.get_page_size() == 10


def test_main_window_show_records_updates_table_and_labels(qapp):
    window = MainWindow()
    records = [
        StudentRecord("Иванов Иван Иванович", "ПИ-21", [1] * 10),
        StudentRecord("Петров Петр Петрович", "ПИ-22", [2] * 10),
    ]

    window.show_records(records, current_page=1, total_pages=2, total_items=12)

    assert window.table.rowCount() == 2
    assert window.table.item(0, 0).text() == "Иванов Иван Иванович"
    assert window.table.item(0, 1).text() == "ПИ-21"
    assert window.table.item(0, 12).text() == "10"
    assert window.page_info_label.text() == "Страница 1 из 2"
    assert window.total_info_label.text() == "Всего записей: 12"


def test_add_record_dialog_creates_record(qapp):
    dialog = AddRecordDialog()

    dialog.full_name_edit.setText("Иванов Иван Иванович")
    dialog.group_edit.setText("ПИ-21")

    for i, spin in enumerate(dialog.semester_spins):
        spin.setValue(i + 1)

    record = dialog.get_record()

    assert record.full_name == "Иванов Иван Иванович"
    assert record.group == "ПИ-21"
    assert record.social_work == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_add_record_dialog_accept_success(qapp):
    dialog = AddRecordDialog()

    dialog.full_name_edit.setText("Иванов Иван Иванович")
    dialog.group_edit.setText("ПИ-21")

    dialog._on_accept()

    assert dialog.result() == dialog.Accepted


def test_add_record_dialog_accept_shows_error(monkeypatch, qapp):
    dialog = AddRecordDialog()

    called = {"count": 0}

    def fake_critical(*args, **kwargs):
        called["count"] += 1

    monkeypatch.setattr("views.add_record_dialog.QMessageBox.critical", fake_critical)

    dialog.full_name_edit.setText("")
    dialog.group_edit.setText("ПИ-21")

    dialog._on_accept()

    assert called["count"] == 1
    assert dialog.result() != dialog.Accepted


def test_add_record_dialog_cancel_button_rejects(qapp):
    dialog = AddRecordDialog()

    dialog.cancel_button.click()

    assert dialog.result() == dialog.Rejected


def test_delete_dialog_fills_groups(qapp):
    repository = make_repository()
    dialog = DeleteDialog(repository=repository)

    items = [dialog.group_combo.itemText(i) for i in range(dialog.group_combo.count())]

    assert "Не выбрано" in items
    assert "ПИ-21" in items
    assert "ПИ-22" in items


def test_delete_dialog_build_criteria_without_range(qapp):
    repository = make_repository()
    dialog = DeleteDialog(repository=repository)

    dialog.surname_edit.setText("Иванов")
    dialog.group_combo.setCurrentIndex(1)

    criteria = dialog._build_criteria()

    assert criteria.surname == "Иванов"
    assert criteria.group in {"ПИ-21", "ПИ-22"}
    assert criteria.min_total is None
    assert criteria.max_total is None


def test_delete_dialog_build_criteria_with_range(qapp):
    repository = make_repository()
    dialog = DeleteDialog(repository=repository)

    dialog.surname_edit.setText("Петров")
    dialog.group_combo.setCurrentIndex(2 if dialog.group_combo.count() > 2 else 1)
    dialog.min_spin.setValue(10)
    dialog.max_spin.setValue(30)

    criteria = dialog._build_criteria()

    assert criteria.surname == "Петров"
    assert criteria.min_total == 10
    assert criteria.max_total == 30


def test_delete_dialog_perform_delete(qapp):
    repository = make_repository()
    dialog = DeleteDialog(repository=repository)

    dialog.surname_edit.setText("Иванов")

    deleted_count = dialog.perform_delete()

    assert deleted_count == 1
    assert len(repository.get_all()) == 2


def test_delete_dialog_perform_delete_without_repository(qapp):
    dialog = DeleteDialog(repository=None)

    deleted_count = dialog.perform_delete()

    assert deleted_count == 0


def test_delete_dialog_buttons(qapp):
    repository = make_repository()
    dialog = DeleteDialog(repository=repository)

    dialog.cancel_button.click()
    assert dialog.result() == dialog.Rejected

    dialog = DeleteDialog(repository=repository)
    dialog.delete_button.click()
    assert dialog.result() == dialog.Accepted


def test_search_dialog_fills_groups(qapp):
    repository = make_repository()
    dialog = SearchDialog(repository=repository)

    items = [dialog.group_combo.itemText(i) for i in range(dialog.group_combo.count())]

    assert "Не выбрано" in items
    assert "ПИ-21" in items
    assert "ПИ-22" in items


def test_search_dialog_build_criteria_without_range(qapp):
    repository = make_repository()
    dialog = SearchDialog(repository=repository)

    dialog.surname_edit.setText("Иванов")

    criteria = dialog._build_criteria()

    assert criteria.surname == "Иванов"
    assert criteria.group is None
    assert criteria.min_total is None
    assert criteria.max_total is None


def test_search_dialog_build_criteria_with_range(qapp):
    repository = make_repository()
    dialog = SearchDialog(repository=repository)

    dialog.surname_edit.setText("Петров")
    dialog.min_spin.setValue(10)
    dialog.max_spin.setValue(30)

    criteria = dialog._build_criteria()

    assert criteria.surname == "Петров"
    assert criteria.min_total == 10
    assert criteria.max_total == 30


def test_search_dialog_perform_search_by_surname(qapp):
    repository = make_repository()
    dialog = SearchDialog(repository=repository)

    dialog.surname_edit.setText("Иванов")
    dialog.perform_search()

    assert dialog.table.rowCount() == 1
    assert dialog.table.item(0, 0).text() == "Иванов Иван Иванович"
    assert dialog.total_info_label.text() == "Всего записей: 1"


def test_search_dialog_perform_search_without_repository(qapp):
    dialog = SearchDialog(repository=None)

    dialog.perform_search()

    assert dialog.table.rowCount() == 0
    assert dialog.total_info_label.text() == "Всего записей: 0"


def test_search_dialog_refresh_table_updates_labels(qapp):
    repository = make_repository()
    dialog = SearchDialog(repository=repository)

    dialog.search_results = repository.get_all()
    dialog.paginator.items = dialog.search_results
    dialog.paginator.current_page = 1

    dialog._refresh_table()

    assert dialog.table.rowCount() == 3
    assert dialog.page_info_label.text() == "Страница 1 из 1"
    assert dialog.total_info_label.text() == "Всего записей: 3"


def test_search_dialog_pagination_methods(qapp):
    repository = RecordRepository()
    for i in range(25):
        repository.add(StudentRecord(f"Студент {i}", "ПИ-21", [1] * 10))

    dialog = SearchDialog(repository=repository)
    dialog.perform_search()

    assert dialog.paginator.current_page == 1

    dialog.go_to_next_page()
    assert dialog.paginator.current_page == 2

    dialog.go_to_last_page()
    assert dialog.paginator.current_page == 3

    dialog.go_to_previous_page()
    assert dialog.paginator.current_page == 2

    dialog.go_to_first_page()
    assert dialog.paginator.current_page == 1


def test_search_dialog_change_page_size(qapp):
    repository = RecordRepository()
    for i in range(25):
        repository.add(StudentRecord(f"Студент {i}", "ПИ-21", [1] * 10))

    dialog = SearchDialog(repository=repository)
    dialog.perform_search()
    dialog.change_page_size(20)

    assert dialog.paginator.page_size == 20
    assert dialog.paginator.current_page == 1


def test_search_dialog_close_button_rejects(qapp):
    repository = make_repository()
    dialog = SearchDialog(repository=repository)

    dialog.close_button.click()

    assert dialog.result() == dialog.Rejected