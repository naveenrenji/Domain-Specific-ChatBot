from flask import Flask, request, jsonify, session
from chatbot import get_validation, get_feasibility, get_novelty
from flask_cors import CORS

from flask_session import Session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
# import config

from pymongo import MongoClient 
import os
from dotenv import load_dotenv

app = Flask(__name__)
# CORS(app)

app = Flask(__name__)
load_dotenv()
# print(config.ApplicationConfig)
# app.config.from_object(config.ApplicationConfig)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

# print(app.config)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
server_session  = Session(app)

MONGO_URI = os.environ.get('MONGO_URI')
# connecting to the mongoDb client 
cluster = MongoClient(MONGO_URI)
# giving the cluster name 
db      = cluster['domain-specific-chatbot']
# giving the collection name 
col     = db['users']

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
    
    return jsonify({'response': response, 'valid': True})


@app.route("/auth/getuser/<email>", methods=['GET'])
def get_user(email):
    print(email)
    user = col.find_one({'email': email})
    # print(user)
    # user.pop('_id')
    # print(user)
    if user != None:
        return user
    else:
        return None
    
@app.route("/auth/profile")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = col.find_one({'email': user_id})
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
        if temp_user != None:
            return {"Error": "User already exists"}
        
        hashed_password = bcrypt.generate_password_hash(password)
        
        print(name)
        new_user = {
            "name": name,
            "email": email,
            "password": hashed_password
        }
        col.insert_one(new_user)
        print(new_user)
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
    print('USER:', user)
    if user == None:
        return jsonify({"Error": "User does not exist"}), 401
    elif not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"error": "Either the email or password is wrong"}), 401
    else:
        session["user_id"] = user['email']
        return jsonify({
            "name": user['name'],
            "email": user['email'],
        }), 200
        
    
@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"