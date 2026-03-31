from src.services.testing_service import TestingService
from src.services.grading_service import GradingService
from src.domain.models import Feedback, Question, Test


class CliMenu:

    def __init__(self, repo):
        self.repo = repo
        self.testing = TestingService(repo)
        self.grading = GradingService(repo)
        self.teacher_password = "teacher123"

    def check_teacher_access(self):
        pwd = input("Teacher password: ")
        if pwd != self.teacher_password:
            print("Access denied.")
            return False
        return True

    def teacher_panel(self):
        if not self.check_teacher_access():
            return

        while True:
            print("\n--- Teacher Panel ---")
            print("1 Create test")
            print("2 Delete test")
            print("3 Edit test title")
            print("4 Back")

            choice = input("Select: ")

            if choice == "1":
                test_id = input("Test id: ")
                title = input("Title: ")
                qn = int(input("Number of questions: "))
                questions = []

                for _ in range(qn):
                    q_id = input("Question id: ")
                    text = input("Question text: ")
                    opt_n = int(input("Number of options: "))
                    options = []

                    for i in range(opt_n):
                        options.append(input(f"Option {i+1}: "))

                    correct = int(input("Correct option number: ")) - 1

                    questions.append(
                        Question(
                            id=q_id,
                            text=text,
                            options=options,
                            correct_index=correct
                        )
                    )

                test = Test(id=test_id, title=title, questions=questions)
                self.repo.add_test(test)
                print("Test created.")

            elif choice == "2":
                test_id = input("Test id to delete: ")

                if test_id in self.repo.data["tests"]:
                    del self.repo.data["tests"][test_id]
                    self.repo._save()
                    print("Test deleted.")
                else:
                    print("Test not found.")

            elif choice == "3":
                test_id = input("Test id: ")

                if test_id not in self.repo.data["tests"]:
                    print("Test not found.")
                    continue

                new_title = input("New title: ")
                self.repo.data["tests"][test_id]["title"] = new_title
                self.repo._save()
                print("Test updated.")

            elif choice == "4":
                return

            else:
                print("Unknown option.")

    def run(self):
        while True:

            print("\n--- Knowledge Testing System ---")
            print("1 List tests")
            print("2 Start test")
            print("3 Grade attempt")
            print("4 Add feedback")
            print("5 Teacher panel")
            print("0 Exit")

            choice = input("Select: ")

            if choice == "1":
                tests = self.repo.list_tests()

                if not tests:
                    print("No tests available.")
                else:
                    for t in tests:
                        print(f"{t.id} - {t.title}")

            elif choice == "2":
                student = input("Student id: ")
                test_id = input("Test id: ")

                try:
                    test = self.repo.get_test(test_id)
                except KeyError:
                    print("Test not found.")
                    continue

                attempt = self.testing.start_attempt(student, test_id)

                for q in test.questions:

                    print(f"\n{q.text}")

                    for i, opt in enumerate(q.options):
                        print(i + 1, opt)

                    try:
                        ans = int(input("Answer: ")) - 1
                    except ValueError:
                        print("Invalid input.")
                        continue

                    self.testing.answer(attempt.id, q.id, ans)

                self.testing.submit(attempt.id)

                print("Attempt submitted:", attempt.id)

            elif choice == "3":
                attempt_id = input("Attempt id: ")

                try:
                    grade = self.grading.grade_attempt(attempt_id)
                except KeyError:
                    print("Attempt not found.")
                    continue

                print("Grade:", grade.value)

                fb = self.repo.data["feedback"].get(attempt_id)
                if fb:
                    print("Feedback:", fb["message"])

            elif choice == "4":
                if not self.check_teacher_access():
                    continue

                attempt_id = input("Attempt id: ")
                teacher_id = input("Teacher id: ")
                message = input("Feedback: ")

                feedback = Feedback(
                    attempt_id=attempt_id,
                    teacher_id=teacher_id,
                    message=message
                )

                self.repo.save_feedback(feedback)
                print("Feedback saved.")

            elif choice == "5":
                self.teacher_panel()

            elif choice == "0":
                break

            else:
                print("Unknown option.")