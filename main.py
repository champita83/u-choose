
from flask import Flask, request, jsonify
from prompts import get_next_prompt
from db import init_db, save_message, create_chat, get_saved_chats, get_chat_history, delete_chat
import openai
import os

app = Flask(__name__)
init_db()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    session_id = request.json.get('session_id')
    riddle_toggle = request.json.get('riddle')
    insight_toggle = request.json.get('insight')

    # Save user message
    save_message(session_id, 'user', user_input)

    # Use GPT for reflection if insight is on
    if insight_toggle:
        prompt = f"The user said: '{user_input}'. Offer a short, reflective insight that could help them understand their internal conflict."
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a gentle, insightful coach helping people see their internal motivations clearly."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = gpt_response['choices'][0]['message']['content'].strip()
    else:
        reply = get_next_prompt(get_chat_history(session_id), riddle_toggle, insight_toggle)

    save_message(session_id, 'assistant', reply)
    return jsonify({'response': reply})

@app.route('/save_chat', methods=['POST'])
def save_chat():
    session_id = request.json.get('session_id')
    name = request.json.get('name')
    create_chat(session_id, name)
    return jsonify({'status': 'success'})

@app.route('/load_chats', methods=['GET'])
def load_chats():
    chats = get_saved_chats()
    return jsonify({'chats': chats})

@app.route('/load_chat/<session_id>', methods=['GET'])
def load_chat(session_id):
    messages = get_chat_history(session_id)
    return jsonify({'messages': messages})

@app.route('/delete_chat/<session_id>', methods=['DELETE'])
def delete_chat_route(session_id):
    delete_chat(session_id)
    return jsonify({'status': 'deleted'})

if __name__ == '__main__':
    app.run(debug=True)
