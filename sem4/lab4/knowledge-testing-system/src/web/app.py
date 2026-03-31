from flask import Flask, render_template, request, redirect, session
from pathlib import Path

from src.storage.json_repo import JsonRepository
from src.services.testing_service import TestingService
from src.services.grading_service import GradingService
from src.domain.models import Test, Question, Feedback

app = Flask(__name__, template_folder="templates")
app.secret_key = "secret123"

repo = JsonRepository(Path("data/storage.json"))
testing = TestingService(repo)
grading = GradingService(repo)

TEACHER_PASSWORD = "teacher123"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tests")
def tests():
    tests = repo.list_tests()
    return render_template("tests.html", tests=tests)


@app.route("/feedback", methods=["GET", "POST"])
def feedback_view():
    if request.method == "POST":
        attempt_id = request.form.get("attempt_id")

        if not attempt_id:
            return render_template(
                "feedback.html",
                attempt_id=None,
                score=None,
                feedback=None,
                not_found=False
            )

        attempt = repo.data["attempts"].get(attempt_id)

        if not attempt:
            return render_template(
                "feedback.html",
                attempt_id=attempt_id,
                score=None,
                feedback=None,
                not_found=True
            )

        grade_data = repo.data["grades"].get(attempt_id)
        score = grade_data["value"] if grade_data else "Not graded"

        feedback_data = repo.data["feedback"].get(attempt_id)
        feedback = feedback_data["message"] if feedback_data else None

        return render_template(
            "feedback.html",
            attempt_id=attempt_id,
            score=score,
            feedback=feedback,
            not_found=False
        )

    return render_template(
        "feedback.html",
        attempt_id=None,
        score=None,
        feedback=None,
        not_found=False
    )


@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    if request.method == "POST":
        password = request.form.get("password")

        if password == TEACHER_PASSWORD:
            session["teacher"] = True
            return redirect("/teacher")

        return render_template("teacher_login.html", error=True)

    if not session.get("teacher"):
        return render_template("teacher_login.html", error=False)

    tests = repo.list_tests()
    return render_template("teacher.html", tests=tests)


@app.route("/logout")
def logout():
    session.pop("teacher", None)
    return redirect("/")


@app.route("/test/<test_id>", methods=["GET", "POST"])
def take_test(test_id):
    test = repo.get_test(test_id)

    if request.method == "POST":
        student = request.form.get("student_id")

        attempt = testing.start_attempt(student, test_id)

        for q in test.questions:
            ans = request.form.get(q.id)
            if ans is not None:
                testing.answer(attempt.id, q.id, int(ans))

        testing.submit(attempt.id)

        grade = grading.grade_attempt(attempt.id)

        return render_template(
            "result.html",
            attempt_id=attempt.id,
            score=grade.value
        )

    return render_template("take_test.html", test=test)


@app.route("/teacher/create", methods=["POST"])
def create_test():
    if not session.get("teacher"):
        return redirect("/")

    test_id = request.form.get("test_id")
    title = request.form.get("title")

    try:
        q_count = int(request.form.get("q_count", "0"))
    except ValueError:
        return redirect("/teacher")

    questions = []

    for i in range(q_count):
        q_text = request.form.get(f"q_text_{i}", "").strip()

        try:
            opt_count = int(request.form.get(f"opt_count_{i}", "0"))
        except ValueError:
            continue

        options = []
        for j in range(opt_count):
            value = request.form.get(f"opt_{i}_{j}", "").strip()
            if value:
                options.append(value)

        try:
            correct = int(request.form.get(f"correct_{i}", "0")) - 1
        except ValueError:
            continue

        if not q_text or len(options) < 2:
            continue

        if correct < 0 or correct >= len(options):
            continue

        question = Question(
            id=f"q{i + 1}",
            text=q_text,
            options=options,
            correct_index=correct
        )

        questions.append(question)

    if not test_id or not title or not questions:
        return redirect("/teacher")

    test = Test(
        id=test_id,
        title=title,
        questions=questions
    )

    repo.add_test(test)

    return redirect("/teacher")


@app.route("/teacher/delete", methods=["POST"])
def delete_test():
    if not session.get("teacher"):
        return redirect("/")

    test_id = request.form.get("test_id")

    if test_id in repo.data["tests"]:
        del repo.data["tests"][test_id]
        repo._save()

    return redirect("/teacher")


@app.route("/teacher/feedback", methods=["POST"])
def add_feedback():
    if not session.get("teacher"):
        return redirect("/")

    attempt_id = request.form.get("attempt_id")
    message = request.form.get("message")

    if attempt_id and message:
        feedback = Feedback(
            attempt_id=attempt_id,
            teacher_id="t1",
            message=message
        )
        repo.save_feedback(feedback)

    return redirect("/teacher")


if __name__ == "__main__":
    app.run(debug=True)