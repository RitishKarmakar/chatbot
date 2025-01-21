from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import mysql.connector  # Using MySQL Connector

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Secret key for session management

# Simulated admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

# MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",       
        user="root",             
        password="root",  
        database="book"         
    )

# Public page
@app.route("/")
def index():
    return redirect(url_for("login"))

# Admin page (protected)
@app.route("/2063d112e46b326178d70cf7aba81fad42a8bcd8e096d765cb6af02809dde325", methods=["GET", "POST"])
def admin_page():
    if "admin" in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        conn.close()
        return render_template("admin.html", books=books)
    else:
        return redirect(url_for("login"))

# Add book route
@app.route("/add_book", methods=["POST"])
def add_book():
    if "2063d112e46b326178d70cf7aba81fad42a8bcd8e096d765cb6af02809dde325" in session:
        title = request.form["title"]
        author = request.form["author"]
        publication_year = request.form["publication_year"]
        copies_available = request.form["copies_available"]
        department = request.form["department"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, publication_year, copies_available, department) VALUES (%s, %s, %s, %s, %s)",
            (title, author, publication_year, copies_available, department)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("admin_page"))
    else:
        return redirect(url_for("login"))

# Delete book route
@app.route("/delete_book/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    if "2063d112e46b326178d70cf7aba81fad42a8bcd8e096d765cb6af02809dde325" in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
        conn.commit()
        conn.close()

        return redirect(url_for("admin_page"))
    else:
        return redirect(url_for("login"))

# Login page for admin
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["2063d112e46b326178d70cf7aba81fad42a8bcd8e096d765cb6af02809dde325"] = True
            return redirect(url_for("admin_page"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("2063d112e46b326178d70cf7aba81fad42a8bcd8e096d765cb6af02809dde325", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
