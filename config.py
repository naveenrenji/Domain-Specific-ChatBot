from dotenv import load_dotenv
import os
# import redis

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    secret_key = os.environ.get('SECRET_KEY')