from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import mysql.connector  # Using MySQL Connector

app = Flask(__name__)
app.secret_key = ""  # Secret key for session management

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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books ORDER BY department")
    books = cursor.fetchall()
    conn.close()
    return render_template("test.html", books=books)

# Admin page (protected)
@app.route("/admin", methods=["GET", "POST"])
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
    if "admin" in session:
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

# Chatbot route for handling user input
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").lower()

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Search for matches in the `books` table
    cursor.execute(
        "SELECT book_id, title, department FROM books WHERE LOWER(title) LIKE %s OR LOWER(department) LIKE %s",
        (f"%{message}%", f"%{message}%")
    )
    matches = cursor.fetchall()
    conn.close()

    # If matches are found, return them as options
    if matches:
        options = []
        for match in matches:
            options.append({
                "text": f"{match['title']} ({match['department']})",
                "link": f"#{match['book_id']}"  # Use the book_id as an anchor for scrolling
            })
        response = {
            "responseType": "options",
            "options": options
        }
    else:
        # No matches found
        response = {
            "responseType": "text",
            "response": "Sorry, I couldn't find any matching books or departments."
        }

    return jsonify(response)

# Login page for admin
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_page"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
