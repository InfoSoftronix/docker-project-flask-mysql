from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os

def create_app():
    app = Flask(__name__)

    # Secret key (required)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret")

    # MySQL Configuration (Docker friendly)
    app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "mysql")
    app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "root")
    app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "root")
    app.config["MYSQL_DB"] = os.getenv("MYSQL_DB", "student")
    app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT", 3306))

    mysql = MySQL(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/reg")
    def regPage():
        return render_template("registration.html")

    @app.route("/saveReg", methods=["POST"])
    def regSaveData():
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO students
                (srollNo, sname, scourse, sduration, saddr)
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    request.form["srollNo"],
                    request.form["sname"],
                    request.form["scourse"],
                    request.form["sduration"],
                    request.form["saddr"],
                ),
            )
            mysql.connection.commit()
        finally:
            cursor.close()

        return redirect(url_for("index"))

    @app.route("/show")
    def showPage():
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()
        finally:
            cursor.close()

        return render_template("view.html", student=students)

    @app.route("/delete/<int:srollNo>")
    def deleteStudent(srollNo):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("DELETE FROM students WHERE srollNo=%s", (srollNo,))
            mysql.connection.commit()
        finally:
            cursor.close()

        return redirect(url_for("showPage"))

    @app.route("/edit/<int:srollNo>")
    def editPage(srollNo):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("SELECT * FROM students WHERE srollNo=%s", (srollNo,))
            student = cursor.fetchone()
        finally:
            cursor.close()

        return render_template("edit.html", student=student)

    @app.route("/update", methods=["POST"])
    def updateSaveData():
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
                """
                UPDATE students
                SET sname=%s, scourse=%s, sduration=%s, saddr=%s
                WHERE srollNo=%s
                """,
                (
                    request.form["sname"],
                    request.form["scourse"],
                    request.form["sduration"],
                    request.form["saddr"],
                    request.form["srollNo"],
                ),
            )
            mysql.connection.commit()
        finally:
            cursor.close()

        return redirect(url_for("showPage"))

    return app


app = create_app()
