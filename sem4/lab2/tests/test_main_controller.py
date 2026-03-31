from controllers.main_controller import MainController
from models.student_record import StudentRecord
from views.main_window import MainWindow


class DummyAddDialog:
    def __init__(self, parent=None):
        self.parent = parent

    def exec_(self):
        return True

    def get_record(self):
        return StudentRecord("Иванов Иван Иванович", "ПИ-21", [1] * 10)


class DummyRejectAddDialog:
    def __init__(self, parent=None):
        self.parent = parent

    def exec_(self):
        return False


class DummyDeleteDialog:
    def __init__(self, parent=None, repository=None):
        self.parent = parent
        self.repository = repository

    def exec_(self):
        return True

    def perform_delete(self):
        return 1


class DummyDeleteZeroDialog:
    def __init__(self, parent=None, repository=None):
        self.parent = parent
        self.repository = repository

    def exec_(self):
        return True

    def perform_delete(self):
        return 0


class DummyRejectDeleteDialog:
    def __init__(self, parent=None, repository=None):
        self.parent = parent
        self.repository = repository

    def exec_(self):
        return False

    def perform_delete(self):
        return 0


class DummySearchDialog:
    def __init__(self, parent=None, repository=None):
        self.parent = parent
        self.repository = repository
        self.executed = False

    def exec_(self):
        self.executed = True
        return 1


def test_main_controller_add_record(qapp):
    window = MainWindow()
    controller = MainController(window)

    record = StudentRecord("Иванов Иван Иванович", "ПИ-21", [1] * 10)
    controller.add_record(record)

    assert len(controller.repository.get_all()) == 1
    assert window.table.rowCount() == 1


def test_main_controller_open_add_dialog_accept(qapp):
    window = MainWindow()
    controller = MainController(window, add_dialog_class=DummyAddDialog)

    controller.open_add_dialog()

    assert len(controller.repository.get_all()) == 1
    assert window.table.rowCount() == 1


def test_main_controller_open_add_dialog_reject(qapp):
    window = MainWindow()
    controller = MainController(window, add_dialog_class=DummyRejectAddDialog)

    controller.open_add_dialog()

    assert len(controller.repository.get_all()) == 0


def test_main_controller_open_add_dialog_without_class(monkeypatch, qapp):
    window = MainWindow()
    controller = MainController(window)

    called = {"info": 0}

    def fake_information(*args, **kwargs):
        called["info"] += 1

    monkeypatch.setattr("controllers.main_controller.QMessageBox.information", fake_information)

    controller.open_add_dialog()

    assert called["info"] == 1


def test_main_controller_open_search_dialog(qapp):
    window = MainWindow()
    controller = MainController(window, search_dialog_class=DummySearchDialog)

    controller.open_search_dialog()

    assert True


def test_main_controller_open_search_dialog_without_class(monkeypatch, qapp):
    window = MainWindow()
    controller = MainController(window)

    called = {"info": 0}

    def fake_information(*args, **kwargs):
        called["info"] += 1

    monkeypatch.setattr("controllers.main_controller.QMessageBox.information", fake_information)

    controller.open_search_dialog()

    assert called["info"] == 1


def test_main_controller_open_delete_dialog_accept(monkeypatch, qapp):
    window = MainWindow()
    controller = MainController(window, delete_dialog_class=DummyDeleteDialog)

    called = {"info": 0}

    def fake_information(*args, **kwargs):
        called["info"] += 1

    monkeypatch.setattr("controllers.main_controller.QMessageBox.information", fake_information)

    controller.open_delete_dialog()

    assert called["info"] == 1


def test_main_controller_open_delete_dialog_zero(monkeypatch, qapp):
    window = MainWindow()
    controller = MainController(window, delete_dialog_class=DummyDeleteZeroDialog)

    called = {"info": 0}

    def fake_information(*args, **kwargs):
        called["info"] += 1

    monkeypatch.setattr("controllers.main_controller.QMessageBox.information", fake_information)

    controller.open_delete_dialog()

    assert called["info"] == 1


def test_main_controller_open_delete_dialog_reject(qapp):
    window = MainWindow()
    controller = MainController(window, delete_dialog_class=DummyRejectDeleteDialog)

    controller.open_delete_dialog()

    assert True


def test_main_controller_open_delete_dialog_without_class(monkeypatch, qapp):
    window = MainWindow()
    controller = MainController(window)

    called = {"info": 0}

    def fake_information(*args, **kwargs):
        called["info"] += 1

    monkeypatch.setattr("controllers.main_controller.QMessageBox.information", fake_information)

    controller.open_delete_dialog()

    assert called["info"] == 1


def test_main_controller_pagination_buttons(qapp):
    window = MainWindow()
    controller = MainController(window)

    for i in range(25):
        controller.add_record(StudentRecord(f"Студент {i}", "ПИ-21", [1] * 10))

    controller.go_to_next_page()
    assert controller.paginator.current_page == 2

    controller.go_to_last_page()
    assert controller.paginator.current_page == 3

    controller.go_to_previous_page()
    assert controller.paginator.current_page == 2

    controller.go_to_first_page()
    assert controller.paginator.current_page == 1


def test_main_controller_change_page_size(qapp):
    window = MainWindow()
    controller = MainController(window)

    for i in range(25):
        controller.add_record(StudentRecord(f"Студент {i}", "ПИ-21", [1] * 10))

    controller.change_page_size(20)

    assert controller.paginator.page_size == 20
    assert controller.paginator.current_page == 1


def test_main_controller_save_to_file_success(monkeypatch, tmp_path, qapp):
    window = MainWindow()
    controller = MainController(window)

    controller.add_record(StudentRecord("Иванов Иван Иванович", "ПИ-21", [1] * 10))

    file_path = tmp_path / "data.xml"

    monkeypatch.setattr(
        "controllers.main_controller.QFileDialog.getSaveFileName",
        lambda *args, **kwargs: (str(file_path), "XML Files (*.xml)")
    )

    called = {"info": 0}

    def fake_information(*args, **kwargs):
        called["info"] += 1

    monkeypatch.setattr("controllers.main_controller.QMessageBox.information", fake_information)

    controller.save_to_file()

    assert file_path.exists()
    assert called["info"] == 1


def test_main_controller_save_to_file_cancel(monkeypatch, qapp):
    window = MainWindow()
    controller = MainController(window)

    monkeypatch.setattr(
        "controllers.main_controller.QFileDialog.getSaveFileName",
        lambda *args, **kwargs: ("", "")
    )

    controller.save_to_file()

    assert True


def test_main_controller_save_to_file_error(monkeypatch, tmp_path, qapp):
    window = MainWindow()
    controller = MainController(window)

    file_path = tmp_path / "data.xml"

    monkeypatch.setattr(
        "controllers.main_controller.QFileDialog.getSaveFileName",
        lambda *args, **kwargs: (str(file_path), "XML Files (*.xml)")
    )

    def fake_save(*args, **kwargs):
        raise Exception("save error")

    monkeypatch.setattr(controller.xml_service, "save", fake_save)

    called = {"critical": 0}

    def fake_critical(*args, **kwargs):
        called["critical"] += 1

    monkeypatch.setattr("controllers.main_controller.QMessageBox.critical", fake_critical)

    controller.save_to_file()

    assert called["critical"] == 1


def test_main_controller_load_from_file_success(monkeypatch, tmp_path, qapp):
    window = MainWindow()
    controller = MainController(window)

    file_path = tmp_path / "data.xml"
    file_path.write_text("<students></students>", encoding="utf-8")

    records = [StudentRecord("Иванов Иван Иванович", "ПИ-21", [1] * 10)]

    monkeypatch.setattr(
        "controllers.main_controller.QFileDialog.getOpenFileName",
        lambda *args, **kwargs: (str(file_path), "XML Files (*.xml)")
    )

    monkeypatch.setattr(controller.xml_service, "load", lambda *args, **kwargs: records)

    called = {"info": 0}

    def fake_information(*args, **kwargs):
        called["info"] += 1

    monkeypatch.setattr("controllers.main_controller.QMessageBox.information", fake_information)

    controller.load_from_file()

    assert len(controller.repository.get_all()) == 1
    assert called["info"] == 1


def test_main_controller_load_from_file_cancel(monkeypatch, qapp):
    window = MainWindow()
    controller = MainController(window)

    monkeypatch.setattr(
        "controllers.main_controller.QFileDialog.getOpenFileName",
        lambda *args, **kwargs: ("", "")
    )

    controller.load_from_file()

    assert True


def test_main_controller_load_from_file_error(monkeypatch, tmp_path, qapp):
    window = MainWindow()
    controller = MainController(window)

    file_path = tmp_path / "data.xml"
    file_path.write_text("<students></students>", encoding="utf-8")

    monkeypatch.setattr(
        "controllers.main_controller.QFileDialog.getOpenFileName",
        lambda *args, **kwargs: (str(file_path), "XML Files (*.xml)")
    )

    def fake_load(*args, **kwargs):
        raise Exception("load error")

    monkeypatch.setattr(controller.xml_service, "load", fake_load)

    called = {"critical": 0}

    def fake_critical(*args, **kwargs):
        called["critical"] += 1

    monkeypatch.setattr("controllers.main_controller.QMessageBox.critical", fake_critical)

    controller.load_from_file()

    assert called["critical"] == 1