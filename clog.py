from flask import Flask, request, jsonify,render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("test.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    # Example responses
    if "hello" in user_message:
        return jsonify({
            "responseType": "options",
            "options": [
                {"text": "Go to management", "link": "#management"},
                {"text": "Go to markets", "link": "#markets"},
                {"text": "Search on computer Science", "link": "#computer-science"}
            ]
        })
    else:
        return jsonify({
            "responseType": "text",
            "response": "Sorry, I didn't understand that."
        })

if __name__ == "__main__":
    app.run(debug=True)
