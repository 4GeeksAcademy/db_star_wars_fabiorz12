from flask import Blueprint, jsonify
from models import db, Character, Planet, User, Favorite

api = Blueprint('api', __name__)

@api.route('/people', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    results = list(map(lambda char: char.serialize(), characters))
    return jsonify(results), 200

@api.route('/people/<int:people_id>', methods=['GET'])
def get_character_by_id(people_id):
    character = Character.query.get(people_id)

    if character is None:
        return jsonify({"error": "Character not found"}), 404

    return jsonify(character.serialize()), 200

@api.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    results = list(map(lambda p: p.serialize(), planets))
    return jsonify(results), 200

@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id)
    
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    return jsonify(planet.serialize()), 200

@api.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    results = list(map(lambda user: user.serialize(), users))
    return jsonify(results), 200

@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1 

    favorites = Favorite.query.filter_by(user_id=user_id).all()

    if not favorites:
        return jsonify({"message": "No favorites found for this user."}), 404

    results = list(map(lambda fav: fav.serialize(), favorites))
    return jsonify(results), 200