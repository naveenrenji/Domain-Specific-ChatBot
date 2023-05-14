from flask import Flask, request, jsonify
from chatbot import get_bot_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    context = request.json.get('context', '')
    response = get_bot_response(message, context)
    return jsonify({'response': response})
