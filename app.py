from flask import Flask, request, jsonify,render_template

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('Demi.html')



@app.route('/chat', methods=['POST'])
def chat():
    # Get the message sent from the frontend
    user_message = request.json.get('message', '')

    # Example response logic based on the user message
    if user_message.lower() == 'hello':
        return jsonify({
            'response': 'Hello! How can I help you today?',
            'options': ['Learn about Management', 'Learn about Computer Science', 'Learn about Law']
        })
    elif user_message.lower() == 'learn about management':
        return jsonify({
            'response': 'Management is the process of planning, organizing, leading, and controlling resources...',
            'options': []
        })
    elif user_message.lower() == 'learn about computer science':
        return jsonify({
            'response': 'Computer Science is the study of computers and computational systems...',
            'options': []
        })
    elif user_message.lower() == 'learn about law':
        return jsonify({
            'response': 'Law is the system of rules created and enforced to regulate behavior...',
            'options': []
        })
    else:
        return jsonify({
            'response': 'Sorry, I didn\'t understand that. Can you try asking something else?',
            'options': ['Learn about Management', 'Learn about Computer Science', 'Learn about Law']
        })

if __name__ == '__main__':
    app.run(debug=True)
