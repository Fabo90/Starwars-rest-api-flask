"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    results = []
    for character in characters:
        results.append(character.serialize())
    return jsonify(results), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if character != None:
        return jsonify(character.serialize()), 200
    else:
        return jsonify('invalid character ID'), 400

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    results = []
    for planet in planets:
        results.append(planet.serialize())   
    return jsonify(results), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet != None:
        return jsonify(planet.serialize()), 200
    else:
        return jsonify('invalid planet ID'), 400
    
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    results = []
    for user in users:
        results.append(user.serialize())
    return jsonify(results), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    user = User.query.get(user_id)
    if user is None: 
         return jsonify({"Invalid user ID"}) 
    return jsonify(user.serialize()['favorites']), 200

@app.route('/users/<int:user_id>/favorites/characters/<int:character_id>', methods=['POST', 'DELETE'])
def handle_character(user_id, character_id):
    if request.method == 'POST':
        user = User.query.get(user_id)
        character = Character.query.get(character_id)
        if character == None or user == None:
            return jsonify('Invalid user or character'), 400
        elif character != None or user != None:
            favorite = Favorites(character_id = character_id, user_id = user_id)
            db.session.add(favorite)
            db.session.commit()
            return jsonify("Character added successfully."), 200
    if request.method == 'DELETE':
        favorite = Favorites.query.all()
        character = None
        user = User.query.get(user_id)
        for fav in favorite:
            if fav.serialize()['character_id'] == character_id:
                character = fav
        if character == None or user == None:
            return jsonify("Invalid user or character"), 400
        else:
            db.session.delete(character)
            db.session.commit()
            return jsonify("Character deleted successfully."), 200
        
@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST', 'DELETE'])
def handle_planet(user_id, planet_id):
    if request.method == 'POST':
        user = User.query.get(user_id)
        planet = Planet.query.get(planet_id)
        if planet == None or user == None:
            return jsonify('Invalid user or planet'), 400
        elif planet != None or user != None:
            favorite = Favorites(planet_id = planet_id, user_id = user_id)
            db.session.add(favorite)
            db.session.commit()
            return jsonify("Planet added successfully."), 200
    if request.method == 'DELETE':
        favorite = Favorites.query.all()
        planet = None
        user = User.query.get(user_id)
        for fav in favorite:
            if fav.serialize()['planet_id'] == planet_id:
                planet = fav
        if planet == None or user == None:
            return jsonify("Invalid user or planet"), 400
        else:
            db.session.delete(planet)
            db.session.commit()
            return jsonify("Planet deleted successfully."), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
