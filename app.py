from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db, init_db
from ai import generate_questions, evaluate_answer, generate_follow_up_question


load_dotenv()


app = Flask(__name__)

app.secret_key = "vivamate-secret-key"


init_db()


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        password = request.form["password"]


        hashed_password = generate_password_hash(password)


        conn = get_db()


        try:

            conn.execute(
                """
                INSERT INTO users
                (name, email, password)
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    email,
                    hashed_password
                )
            )

            conn.commit()

        except Exception:

            conn.close()

            return "Email already registered"


        conn.close()


        return redirect(
            url_for("login")
        )


    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]


        conn = get_db()


        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()


        conn.close()


        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]

            session["name"] = user["name"]


            return redirect(
                url_for("dashboard")
            )


        return "Invalid email or password"


    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("index")
    )


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    conn = get_db()


    stats = conn.execute(
        """
        SELECT
            COUNT(*) AS total_vivas,
            AVG(score) AS average_score,
            MAX(score) AS best_score
        FROM sessions
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchone()


    progress = conn.execute(
        """
        SELECT score
        FROM sessions
        WHERE user_id = ?
        ORDER BY created_at ASC
        """,
        (session["user_id"],)
    ).fetchall()


    conn.close()


    average_score = stats["average_score"] or 0

    best_score = stats["best_score"] or 0


    if average_score >= 90:

        performance = "EXCELLENT"

    elif average_score >= 75:

        performance = "VERY GOOD"

    elif average_score >= 60:

        performance = "GOOD"

    else:

        performance = "NEEDS IMPROVEMENT"


    progress_scores = [
        row["score"]
        for row in progress
    ]


    return render_template(
        "dashboard.html",
        name=session["name"],
        total_vivas=stats["total_vivas"],
        average_score=average_score,
        best_score=best_score,
        performance=performance,
        progress_scores=progress_scores
    )


@app.route("/setup", methods=["GET", "POST"])
def setup():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    if request.method == "POST":

        subject = request.form["subject"]

        topic = request.form["topic"]

        difficulty = request.form["difficulty"]

        number = int(
            request.form["number"]
        )


        questions = generate_questions(
            subject,
            topic,
            difficulty,
            number
        )


        conn = get_db()


        cursor = conn.execute(
            """
            INSERT INTO sessions
            (
                user_id,
                subject,
                topic,
                difficulty,
                total_questions
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                subject,
                topic,
                difficulty,
                number
            )
        )


        session_id = cursor.lastrowid


        for question in questions:

            conn.execute(
                """
                INSERT INTO questions
                (session_id, question)
                VALUES (?, ?)
                """,
                (
                    session_id,
                    question
                )
            )


        conn.commit()

        conn.close()


        session["viva_session_id"] = session_id

        session["viva_followup"] = False


        return redirect(
            url_for("viva")
        )


    return render_template(
        "setup.html"
    )


@app.route("/viva", methods=["GET", "POST"])
def viva():

    if "viva_session_id" not in session:

        return redirect(
            url_for("setup")
        )


    session_id = session["viva_session_id"]


    conn = get_db()


    questions = conn.execute(
        """
        SELECT *
        FROM questions
        WHERE session_id = ?
        ORDER BY id
        """
        ,
        (session_id,)
    ).fetchall()


    conn.close()


    current_index = int(
        request.args.get("q", 0)
    )


    if current_index >= len(questions):

        return redirect(
            url_for("result")
        )


    question = questions[current_index]


    if request.method == "POST":

        answer = request.form["answer"]


        evaluation = evaluate_answer(
            question["question"],
            answer
        )


        conn = get_db()


        conn.execute(
            """
            UPDATE questions
            SET answer = ?,
                score = ?,
                feedback = ?,
                ideal_answer = ?,
                improvement = ?
            WHERE id = ?
            """,
            (
                answer,
                evaluation["score"],
                evaluation["feedback"],
                evaluation["ideal_answer"],
                evaluation["improvement"],
                question["id"]
            )
        )


        conn.commit()

        conn.close()


        follow_up = generate_follow_up_question(
            question["question"],
            answer,
            evaluation["score"]
        )


        session["followup_question"] = follow_up

        session["followup_score"] = evaluation["score"]

        session["followup_original_index"] = current_index

        session["viva_followup"] = True


        return redirect(
            url_for(
                "followup",
                q=current_index
            )
        )


    return render_template(
        "viva.html",
        question=question,
        number=current_index + 1,
        total=len(questions)
    )


@app.route("/followup", methods=["GET", "POST"])
def followup():

    if "viva_session_id" not in session:

        return redirect(
            url_for("setup")
        )


    if "followup_question" not in session:

        return redirect(
            url_for("viva")
        )


    current_index = int(
        request.args.get(
            "q",
            session.get(
                "followup_original_index",
                0
            )
        )
    )


    followup_question = session[
        "followup_question"
    ]


    followup_score = session.get(
        "followup_score",
        0
    )


    if request.method == "POST":

        followup_answer = request.form[
            "answer"
        ]


        original_question = ""


        conn = get_db()


        questions = conn.execute(
            """
            SELECT *
            FROM questions
            WHERE session_id = ?
            ORDER BY id
            """,
            (
                session["viva_session_id"],
            )
        ).fetchall()


        if (
            current_index >= 0
            and current_index < len(questions)
        ):

            original_question = questions[
                current_index
            ]["question"]


        if original_question:

            followup_evaluation = evaluate_answer(
                followup_question,
                followup_answer
            )


            current_question_id = questions[
                current_index
            ]["id"]


            existing = conn.execute(
                """
                SELECT improvement
                FROM questions
                WHERE id = ?
                """,
                (
                    current_question_id,
                )
            ).fetchone()


            old_improvement = ""

            if existing:

                old_improvement = (
                    existing["improvement"]
                    or ""
                )


            combined_improvement = (
                old_improvement
                + " Follow-up: "
                + followup_evaluation["improvement"]
            )


            conn.execute(
                """
                UPDATE questions
                SET improvement = ?
                WHERE id = ?
                """,
                (
                    combined_improvement,
                    current_question_id
                )
            )


            conn.commit()


        conn.close()


        session.pop(
            "followup_question",
            None
        )

        session.pop(
            "followup_score",
            None
        )

        session.pop(
            "followup_original_index",
            None
        )

        session["viva_followup"] = False


        next_question = current_index + 1


        return redirect(
            url_for(
                "viva",
                q=next_question
            )
        )


    return render_template(
        "followup.html",
        question=followup_question,
        number=current_index + 1,
        total=1,
        previous_score=followup_score
    )


@app.route("/result")
def result():

    if "viva_session_id" not in session:

        return redirect(
            url_for("dashboard")
        )


    session_id = session[
        "viva_session_id"
    ]


    conn = get_db()


    questions = conn.execute(
        """
        SELECT *
        FROM questions
        WHERE session_id = ?
        """,
        (session_id,)
    ).fetchall()


    total = len(questions)


    score = sum(
        q["score"] or 0
        for q in questions
    )


    percentage = 0


    if total > 0:

        percentage = (
            score /
            (total * 10)
        ) * 100


    conn.execute(
        """
        UPDATE sessions
        SET score = ?
        WHERE id = ?
        """,
        (
            percentage,
            session_id
        )
    )


    conn.commit()

    conn.close()


    session.pop(
        "followup_question",
        None
    )

    session.pop(
        "followup_score",
        None
    )

    session.pop(
        "followup_original_index",
        None
    )

    session["viva_followup"] = False


    return render_template(
        "result.html",
        questions=questions,
        score=percentage
    )


@app.route("/history")
def history():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    conn = get_db()


    sessions = conn.execute(
        """
        SELECT *
        FROM sessions
        WHERE user_id = ?
        ORDER BY created_at DESC
        """
        ,
        (session["user_id"],)
    ).fetchall()


    conn.close()


    return render_template(
        "history.html",
        sessions=sessions
    )


if __name__ == "__main__":

    app.run(debug=True)