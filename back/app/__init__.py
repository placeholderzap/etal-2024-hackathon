# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.db import db
from app.cidade.controller import cidade_controller
from app.config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    app.register_blueprint(cidade_controller)
    
    return app
