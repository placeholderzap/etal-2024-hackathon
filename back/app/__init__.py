# app/__init__.py
from flask import Flask
from app.db import db
from app.usina.controller import usina_controller
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    app.register_blueprint(usina_controller)
    
    return app
