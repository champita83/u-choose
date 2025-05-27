from flask import Flask, request, jsonify
from prompts import get_next_prompt

app = Flask(__name__)

conversations = {}  # In-memory store; can later be moved to DB

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    session_id = request.json.get('session_id')
    riddle_toggle = request.json.get('riddle')
    insight_toggle = request.json.get('insight')

    if session_id not in conversations:
        conversations[session_id] = []

    conversations[session_id].append({'role': 'user', 'content': user_input})

    response = get_next_prompt(conversations[session_id], riddle_toggle, insight_toggle)

    conversations[session_id].append({'role': 'assistant', 'content': response})

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
