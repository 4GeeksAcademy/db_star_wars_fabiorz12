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

@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  # Simulamos que el usuario logueado es el ID 1

    # Validar si el planeta existe
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    # Verificar si ya es favorito
    existing_fav = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_fav:
        return jsonify({"message": "Planet already in favorites"}), 400

    # Crear nuevo favorito
    new_fav = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"message": "Planet added to favorites"}), 201

@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = 1  # Usuario simulado

    # Validar que el personaje existe
    character = Character.query.get(people_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    # Verificar si ya está en favoritos
    existing_fav = Favorite.query.filter_by(user_id=user_id, character_id=people_id).first()
    if existing_fav:
        return jsonify({"message": "Character already in favorites"}), 400

    # Crear favorito nuevo (planet_id queda None)
    new_fav = Favorite(user_id=user_id, character_id=people_id, planet_id=None)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"message": "Character added to favorites", "favorite": new_fav.serialize()}), 201

@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1  # Simulamos usuario actual

    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "Favorite planet not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": f"Favorite planet with id {planet_id} deleted"}), 200

@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = 1  # Usuario simulado

    favorite = Favorite.query.filter_by(user_id=user_id, character_id=people_id).first()
    if not favorite:
        return jsonify({"error": "Favorite character not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": f"Favorite character with id {people_id} deleted"}), 200