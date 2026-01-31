from flask import Flask
from app.auth.controller import auth_bp
from app.favorites.controller import favorites_bp

def register_routes(app: Flask):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(favorites_bp, url_prefix='/favorites')
