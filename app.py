from flask import Flask, request, jsonify
from flask_cors import CORS
from db import init_db, register_user, authenticate_user, create_chat, save_message, get_chat_history, get_user_chats, delete_chat
from prompts import get_gpt_response

app = Flask(__name__)
CORS(app)
init_db()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if register_user(data['username'], data['password']):
        return jsonify({"message": "User registered"}), 200
    return jsonify({"error": "Username already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = authenticate_user(data['username'], data['password'])
    if user_id:
        return jsonify({"user_id": user_id}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message")
    session_id = data.get("session_id")
    riddle_toggle = data.get("riddle", False)
    insight_toggle = data.get("insight", False)

    save_message(session_id, "user", user_input)
    history = get_chat_history(session_id)
    history.append({'role': 'user', 'content': user_input})
    reply = get_gpt_response(history, riddle_toggle, insight_toggle)
    save_message(session_id, "assistant", reply)
    return jsonify({"response": reply})

@app.route('/save_chat', methods=['POST'])
def save_chat():
    data = request.json
    create_chat(data['user_id'], data['session_id'], data['name'], data.get('journal', ''))
    return jsonify({"status": "success"})

@app.route('/load_chats/<int:user_id>', methods=['GET'])
def load_chats(user_id):
    chats = get_user_chats(user_id)
    return jsonify({"chats": chats})

@app.route('/load_chat/<session_id>', methods=['GET'])
def load_chat(session_id):
    messages = get_chat_history(session_id)
    return jsonify({"messages": messages})

@app.route('/delete_chat/<session_id>', methods=['DELETE'])
def remove_chat(session_id):
    delete_chat(session_id)
    return jsonify({"status": "deleted"})

if __name__ == '__main__':
    app.run(debug=True)
