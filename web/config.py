import os
from dotenv import load_dotenv


load_dotenv()

ENV = os.getenv("FLASK_ENV") or "development"
SECRET_KEY = os.getenv("SECRET_KEY") or "wongxy"
DEBUG = os.getenv("DEBUG") or True