import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import mssql_python

load_dotenv()

app = Flask(__name__)

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_connection():
    return mssql_python.connect(
        server=DB_SERVER,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        encrypt=True
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add_visitor():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        purpose = request.form["purpose"]

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO Visitors (FullName, EmailAddress, Purpose)
                    VALUES (?, ?, ?)
                    """,
                    (full_name, email, purpose)
                )
            conn.commit()

        return redirect(url_for("list_visitors"))

    return render_template("add_visitor.html")

@app.route("/visitors")
def list_visitors():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT Id, FullName, EmailAddress, Purpose, CreatedAt
                FROM Visitors
                ORDER BY Id DESC
                """
            )
            rows = cursor.fetchall()

    return render_template("visitors.html", visitors=rows)

if __name__ == "__main__":
    app.run(debug=True)
