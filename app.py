from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            qualification TEXT,
            percentage REAL,
            skills TEXT,
            interest TEXT,
            preferred_course TEXT,
            career_goal TEXT,
            school_sports_experience TEXT
        )
    """)

    conn.commit()
    conn.close()

create_database()

@app.route("/")
def home():
    return render_template("profile.html")

@app.route("/profile", methods=["POST"])
def profile():
    data = (
        request.form["name"],
        request.form["qualification"],
        request.form["percentage"],
        request.form["skills"],
        request.form["interest"],
        request.form["preferred_course"],
        request.form["career_goal"],
        request.form["school_sports_experience"]
    )

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, qualification, percentage, skills, interest,
         preferred_course, career_goal, school_sports_experience)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()

    return "Student details saved successfully!"

if __name__ == "__main__":
    app.run(debug=True)