from flask import Flask, request, jsonify
from chatbot import get_validation, get_feasibility, get_novelty
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# @app.route('/chat', methods=['POST'])
# def chat():
#     message = request.json['message']
#     context = request.json.get('context', '')
#     response = get_bot_response(message, context)
#     return jsonify({'response': response})


@app.route('/validation', methods=['POST'])
def chat():
    message = request.json['message']
    response = get_validation(message)
    return jsonify({'response': response})

@app.route('/novelty', methods=['POST'])
def chat():
    message = request.json['message']
    response = get_novelty(message)
    return jsonify({'response': response})

@app.route('/feasibility', methods=['POST'])
def chat():
    message = request.json['message']
    response = get_feasibility(message)
    return jsonify({'response': response})