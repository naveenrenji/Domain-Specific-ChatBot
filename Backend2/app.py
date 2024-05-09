from flask import Flask, request, jsonify, session
from Phase2.score2 import get_validation, get_feasibility, get_novelty, get_sentiment
from flask_cors import CORS

import jwt

from flask_session import Session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
# import config

from pymongo import MongoClient 
import os
from dotenv import load_dotenv

_deployed_env_ = os.environ.get("ENVIRONMENT", default=None)

app = Flask(__name__)
load_dotenv()
# print(config.ApplicationConfig)
# app.config.from_object(config.ApplicationConfig)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object('settings')

print(_deployed_env_)

if (_deployed_env_ is None):
    print("dev")
if (_deployed_env_ == 'prod'):
    print('prod')
    app.config.from_pyfile('settings_prod.py')

# print(app.config)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)

server_session  = Session(app)

# print(app.config.get('MONGO_URI'))

MONGO_URI = app.config.get('MONGO_URI')
# connecting to the mongoDb client 
cluster = MongoClient(MONGO_URI)
# giving the cluster name 
db      = cluster['domain-specific-chatbot']
# giving the user_collection name 
user_col     = db['users']
chats_col    = db['user_chats']

@app.route('/test', methods=['GET'])
def test():
    print("Running")
    return jsonify({'response': 'Hello, running on environment: '+ _deployed_env_})


@app.route('/validation', methods=['POST'])
def chatValidation():
    message = request.json['content']
    response = get_validation(message)
    return jsonify({'response': response})

@app.route('/novelty', methods=['POST'])
def chatNovelty():
    message = request.json['content']
    response = get_novelty(message)
    print(response, type(response))
    return jsonify({'response': response})

@app.route('/feasibility', methods=['POST'])
def chatFeasibility():
    message = request.json['content']
    response = get_feasibility(message)
    return jsonify({'response': response})

@app.route('/sentiment', methods=['POST'])
def chatValidation():
    message = request.json['content']
    response = get_sentiment(message)
    return jsonify({'response': response})

@app.route('/chat', methods=['POST'])
def chat():
    response = ''
    message = request.json['content']
    
    validity = get_validation(message)
    if validity == 'no':
        return jsonify({'response': 'The chat input must be related to washing machine', 'valid': False})
    
    novelty = get_novelty(message)
    feasibility = get_feasibility(message)
    
    response = 'Novelty of the idea is '+str(novelty)+' and feasibility is '+str(feasibility)
    
    return jsonify({'response': response, 'valid': True, 'noveltyScore': novelty, 'feasibilityScore': feasibility})


@app.route("/auth/getuser/<email>", methods=['GET'])
def get_user(email):
    print(email)
    user = user_col.find_one({'email': email})
    # print(user)
    # user.pop('_id')
    # print(user)
    if user != None:
        return user
    else:
        return None
    
@app.route("/auth/profile", methods=['GET'])
def get_current_user():
    user_session = session.get("user_id")
    print("sessions:",user_session)
    if not user_session:
        return jsonify({"Error": "Unauthorized"}), 401
    
    user = user_col.find_one({'email': user_session['email']})
    return jsonify({
        "name": user['name'],
        "email": user['email']
    }) 
    

@app.route("/auth/signup", methods=['POST'])
def signup_user():
    try:
        print(request.json)
        password = request.json['password']
        name  = request.json['name']
        email = request.json['email']
        
        temp_user = get_user(email)
        print(temp_user)
        if temp_user != None:
            return {"Error": "Emailid already registered"}
        
        hashed_password = bcrypt.generate_password_hash(password)
        
        print(name)
        new_user = {
            "name": name,
            "email": email,
            "password": hashed_password
        }
        user_col.insert_one(new_user)
        
        new_chats = {
            'email': email,
            'chats': []
        }
        chats_col.insert_one(new_chats)
        
        return {
            "name": name,
            "email": email,
        }
    except:
        return {
            "Error": "Could not register the user"
        }
        
        
@app.route("/auth/login", methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    user = get_user(email)
    
    if user == None:
        return jsonify({"Error": "User with this Email does not exist"}), 200
    
    print('USER:', user)
    str_id = str(user["_id"])
    print(str_id)
    
    
    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"Error": "Either the Email or Password is invalid"}), 200
    else:
        
        token = bcrypt.generate_password_hash(user['email'] + str_id)
        session["user_id"] = {
            "email": user['email'],
            "token": str(token)
        }
        print("Login: ",session)
        return jsonify({
            "name": user['name'],
            "email": user['email'],
            "session_token": str(token)
        }), 200
        
    
@app.route("/auth/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"

@app.route("/save-chat", methods=["POST"])
def chat_save():
    chats = request.json['chats']
    timestamp = request.json['timestamp']
    email = request.json['email']
    
    body = {
        'timestamp': timestamp,
        'chat': chats 
    }
    print(body)
    
    chats_new = chats_col.update_one({'email': email}, {'$push': {'chats': body}})
    
    # for document in chats_new:
    #     print(document)
    print(chats_new.modified_count)
    
    return {"message": "Success"}


@app.route("/get-chats", methods=["POST"])
def get_chats():
    email = request.json['email']
    user_chats = chats_col.find_one({'email': email})
    # user_chats = chats_col.find({})
    # for document in user_chats:
    #     print(document)
    print(user_chats)
    if user_chats is None:
        return []        
    return {'chats': user_chats['chats']}
    
    
    