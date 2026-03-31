import app as app_module
import main as main_module


class FakeQtApp:
    def __init__(self):
        self.exec_called = False

    def exec_(self):
        self.exec_called = True
        return 0


def test_create_app(monkeypatch):
    fake_app_instance = FakeQtApp()

    class FakeWindow:
        def __init__(self):
            self.shown = False
            self.raised = False
            self.activated = False

        def show(self):
            self.shown = True

        def raise_(self):
            self.raised = True

        def activateWindow(self):
            self.activated = True

    class FakeController:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    monkeypatch.setattr(app_module, "QApplication", lambda args: fake_app_instance)
    monkeypatch.setattr(app_module, "MainWindow", FakeWindow)
    monkeypatch.setattr(app_module, "MainController", FakeController)

    result = app_module.create_app()

    assert result is fake_app_instance
    assert hasattr(fake_app_instance, "main_window")
    assert hasattr(fake_app_instance, "main_controller")
    assert fake_app_instance.main_window.shown is True
    assert fake_app_instance.main_window.raised is True
    assert fake_app_instance.main_window.activated is True


def test_main_calls_sys_exit(monkeypatch):
    fake_app = FakeQtApp()

    monkeypatch.setattr(main_module, "create_app", lambda: fake_app)

    result = {"code": None}

    def fake_exit(code):
        result["code"] = code

    monkeypatch.setattr(main_module.sys, "exit", fake_exit)

    main_module.main()

    assert fake_app.exec_called is True
    assert result["code"] == 0