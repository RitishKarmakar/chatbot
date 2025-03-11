from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import mysql.connector  # Using MySQL Connector
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)
app.secret_key = "BE@@#$BBLOPP"  # Secret key for session management

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

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT book_id, title, department FROM books")
    books = cursor.fetchall()
    conn.close()

    corpus = [message] + [book["title"] + " " + book["department"] for book in books]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    query_vector = tfidf_matrix[0]
    doc_vectors = tfidf_matrix[1:]
    similarities = cosine_similarity(query_vector, doc_vectors).flatten()
    
    sorted_books = sorted(zip(books, similarities), key=lambda x: x[1], reverse=True)
    
    TP = 1  # Assuming one relevant document is retrieved
    FP = len(books) - TP
    FN = 0
    TN = 0
    
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    f1_measure = 2 * (precision * recall) / (precision + recall)
    
    print("Query Similarity Results:")
    for book, similarity in sorted_books:
        print(f"Book ID {book['book_id']}: Similarity = {similarity}")
    print(f"Precision: {precision}, Recall: {recall}, Accuracy: {accuracy}, F1 Measure: {f1_measure}")
    
    if sorted_books and sorted_books[0][1] > 0:
        options = [{"text": f"{book['title']} ({book['department']})", "link": f"#{book['book_id']}"} for book, _ in sorted_books]
        response = {"responseType": "options", "options": options}
    else:
        response = {"responseType": "text", "response": "Sorry, I couldn't find any matching books or departments."}
    
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
