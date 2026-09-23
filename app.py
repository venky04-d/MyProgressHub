from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# ---------------- HOME ----------------

@app.route("/")
def home():

    db = sqlite3.connect("tasks.db")

    total_tasks = db.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    completed_tasks = db.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed = 1"
    ).fetchone()[0]

    pending_tasks = total_tasks - completed_tasks

    progress = db.execute(
        "SELECT * FROM progress"
    ).fetchall()

    db.close()

    return render_template(
        "index.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        progress=progress
    )

# ---------------- TASKS ----------------

@app.route("/tasks")
def tasks_page():

    db = sqlite3.connect("tasks.db")

    tasks = db.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    db.close()

    return render_template("tasks.html", tasks=tasks)


@app.route("/add-task-page")
def add_task_page():
    return render_template("add_task.html")


@app.route("/add-task", methods=["POST"])
def add_task():

    task = request.form["task"]

    db = sqlite3.connect("tasks.db")

    db.execute(
        "INSERT INTO tasks (task) VALUES (?)",
        (task,)
    )

    db.commit()
    db.close()

    return redirect("/tasks")


@app.route("/complete-task/<int:task_id>", methods=["POST"])
def complete_task(task_id):

    db = sqlite3.connect("tasks.db")

    db.execute(
        """
        UPDATE tasks
        SET completed = CASE
            WHEN completed = 0 THEN 1
            ELSE 0
        END
        WHERE id = ?
        """,
        (task_id,)
    )

    db.commit()
    db.close()

    return redirect("/tasks")


@app.route("/delete-task/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    db = sqlite3.connect("tasks.db")

    db.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    db.commit()
    db.close()

    return redirect("/tasks")


@app.route("/edit-task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):

    if request.method == "POST":

        new_task = request.form["task"]

        db = sqlite3.connect("tasks.db")

        db.execute(
            "UPDATE tasks SET task = ? WHERE id = ?",
            (new_task, task_id)
        )

        db.commit()
        db.close()

        return redirect("/tasks")

    db = sqlite3.connect("tasks.db")

    task = db.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    db.close()

    return render_template("edit.html", task=task)


# ---------------- NOTES ----------------

@app.route("/notes")
def notes_page():

    db = sqlite3.connect("tasks.db")

    notes = db.execute(
        "SELECT * FROM notes"
    ).fetchall()

    db.close()

    return render_template("notes.html", notes=notes)


@app.route("/add-note-page")
def add_note_page():
    return render_template("add_note.html")


@app.route("/add-note", methods=["POST"])
def add_note():

    note = request.form["note"]

    db = sqlite3.connect("tasks.db")

    db.execute(
        "INSERT INTO notes (note) VALUES (?)",
        (note,)
    )

    db.commit()
    db.close()

    return redirect("/notes")


@app.route("/edit-note/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):

    if request.method == "POST":

        new_note = request.form["note"]

        db = sqlite3.connect("tasks.db")

        db.execute(
            "UPDATE notes SET note = ? WHERE id = ?",
            (new_note, note_id)
        )

        db.commit()
        db.close()

        return redirect("/notes")

    db = sqlite3.connect("tasks.db")

    note = db.execute(
        "SELECT * FROM notes WHERE id = ?",
        (note_id,)
    ).fetchone()

    db.close()

    return render_template("edit_note.html", note=note)


@app.route("/delete-note/<int:note_id>", methods=["POST"])
def delete_note(note_id):

    db = sqlite3.connect("tasks.db")

    db.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    db.commit()
    db.close()

    return redirect("/notes")


# ---------------- PROGRESS ----------------

@app.route("/progress")
def progress_page():

    db = sqlite3.connect("tasks.db")

    progress = db.execute(
        "SELECT * FROM progress"
    ).fetchall()

    db.close()

    return render_template(
        "progress.html",
        progress=progress
    )


@app.route("/add-progress-page")
def add_progress_page():
    return render_template("add_progress.html")


@app.route("/add-progress", methods=["POST"])
def add_progress():

    technology = request.form["technology"]
    topic = request.form["topic"]
    progress_value = request.form["progress"]

    db = sqlite3.connect("tasks.db")

    db.execute(
        """
        INSERT INTO progress
        (technology, topic, progress)
        VALUES (?, ?, ?)
        """,
        (technology, topic, progress_value)
    )

    db.commit()
    db.close()

    return redirect("/progress")


@app.route("/edit-progress/<int:progress_id>", methods=["GET", "POST"])
def edit_progress(progress_id):

    if request.method == "POST":

        technology = request.form["technology"]
        topic = request.form["topic"]
        progress_value = request.form["progress"]

        db = sqlite3.connect("tasks.db")

        db.execute(
            """
            UPDATE progress
            SET technology = ?, topic = ?, progress = ?
            WHERE id = ?
            """,
            (technology, topic, progress_value, progress_id)
        )

        db.commit()
        db.close()

        return redirect("/progress")

    db = sqlite3.connect("tasks.db")

    item = db.execute(
        "SELECT * FROM progress WHERE id = ?",
        (progress_id,)
    ).fetchone()

    db.close()

    return render_template(
        "edit_progress.html",
        item=item
    )


@app.route("/delete-progress/<int:progress_id>", methods=["POST"])
def delete_progress(progress_id):

    db = sqlite3.connect("tasks.db")

    db.execute(
        "DELETE FROM progress WHERE id = ?",
        (progress_id,)
    )

    db.commit()
    db.close()

    return redirect("/progress")


# ---------------- TEST ROUTES ----------------

@app.route("/hello")
def hello():

    return "Hello from Python backend!"


@app.route("/message", methods=["POST"])
def message():

    data = request.form["message"]

    return "Python received: " + data


# ---------------- DATABASE ----------------

def create_database():

    db = sqlite3.connect("tasks.db")


    # Tasks table

    db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)


    # Notes table

    db.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT NOT NULL
        )
    """)


    # Progress table

    db.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            technology TEXT NOT NULL,
            topic TEXT NOT NULL,
            progress INTEGER NOT NULL
        )
    """)


    db.commit()
    db.close()


# Create database and tables

create_database()


# ---------------- START FLASK ----------------

import os

app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 5000))
)