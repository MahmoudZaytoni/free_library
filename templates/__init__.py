from flask import Flask
from flask import Blueprint


def create_app():
    app = Flask(__name__)    
    app.config['SECRET_KET'] = 'secretkey'

    from .auth import auth
    from .
