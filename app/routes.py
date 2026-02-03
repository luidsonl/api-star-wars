from flask import Flask
from app.auth.controller import auth_bp
from app.favorites.controller import favorites_bp
from app.people.controller import people_bp
from app.films.controller import films_bp
from app.planets.controller import planets_bp
from app.species.controller import species_bp
from app.starships.controller import starships_bp
from app.vehicles.controller import vehicles_bp
from app.user.controller import user_bp

def register_routes(app: Flask):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(favorites_bp, url_prefix='/favorites')
    app.register_blueprint(people_bp, url_prefix='/people')
    app.register_blueprint(films_bp, url_prefix='/films')
    app.register_blueprint(planets_bp, url_prefix='/planets')
    app.register_blueprint(species_bp, url_prefix='/species')
    app.register_blueprint(starships_bp, url_prefix='/starships')
    app.register_blueprint(vehicles_bp, url_prefix='/vehicles')
    app.register_blueprint(user_bp, url_prefix='/users')

