from src.storage.repository import Repository


class DummyRepository(Repository):

    def list_tests(self):
        return []

    def get_test(self, test_id):
        pass

    def add_test(self, test):
        pass

    def add_attempt(self, attempt):
        pass

    def get_attempt(self, attempt_id):
        pass

    def update_attempt(self, attempt):
        pass

    def save_grade(self, grade):
        pass

    def save_feedback(self, feedback):
        pass

    def add_student(self, student):
        pass

    def add_teacher(self, teacher):
        pass


def test_repository_interface():

    repo = DummyRepository()

    assert repo.list_tests() == []