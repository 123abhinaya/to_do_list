from flask import Flask, render_template, request, redirect
import sqlite3, time

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_seconds(value, unit):
    if unit == "minutes":
        return value * 60
    if unit == "hours":
        return value * 3600
    if unit == "days":
        return value * 86400
    if unit == "months":
        return value * 2592000


@app.route('/')
def index():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    now = int(time.time())
    updated_tasks = []

    for t in tasks:
        seconds = get_seconds(t["deadline"], t["unit"])
        if seconds is None:
            time_left = 0  # or some default
        else:
            time_left = (t["created_at"] + seconds) - now

        if t["status"] != "Completed":
            if time_left <= 0:
                status = "Overdue"
            else:
                status = "Pending"
        else:
            status = "Completed"

        updated_tasks.append({
            **dict(t),
            "status": status,
            "time_left": time_left
        })

    return render_template("index.html", tasks=updated_tasks)

@app.route('/add', methods=['POST'])
def add():
    try:
        title = request.form['title']
        deadline = int(request.form['deadline'])
        unit = request.form['unit']
        if unit not in ["hours", "days", "months"]:
            unit = "hours"  # default
        created_at = int(time.time())

        conn = get_db()
        conn.execute(
            "INSERT INTO tasks (title, deadline, unit, created_at) VALUES (?,?,?,?)",
            (title, deadline, unit, created_at)
        )
        conn.commit()
        conn.close()
        return redirect('/')
    except ValueError:
        return "Invalid input", 400

@app.route('/complete/<int:id>')
def complete(id):
    conn = get_db()
    conn.execute("UPDATE tasks SET status='Completed' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=False)