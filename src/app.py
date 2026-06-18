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
from models import db, User, People, Planet, Vehicle, Species, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    #app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route ('/people', methods = ['GET'])
def get_all_people ():
   people = People.query.all()
   return jsonify ([person.serialize() for person in people]), 200

@app.route ('/people/<int:people_id>', methods = ['GET'])
def get_character (people_id):
    character = People.query.get (people_id)
    if character is None:
        raise APIException ("Character is not found", status_code = 404)
    return jsonify (character.serialize ()), 200

@app.route ('/planets', methods = ['GET'])
def get_all_planets ():
    planets = Planet.query.all ()
    return jsonify ([planet.serialize () for planet in planets]), 200

@app.route ('/planets/<int:planet_id>', methods = ['GET'])
def get_planet (planet_id):
    planet = Planet.query.get (planet_id)
    if planet is None:
        raise APIException ("Planet is not found", status_code = 404)
    return jsonify (planet.serialize()), 200

@app.route ('/users', methods = ['GET'])
def get_all_users ():
    users = User.query.all ()
    return jsonify ([user.serialize () for user in users]), 200

[GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual.

@app.route ('/users/<int:user_id>/favorites', methods = ['GET'])
def get_all_favorites_from_user (user_id):
    favorites_from_user = Favorite.query.filter_by (user_id = user_id).all ()
    return jsonify ([favorite.serialize () for favorite in favorites_from_user]), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    #app.run(host='0.0.0.0', port=PORT, debug=False)
    app.run(host='0.0.0.0', port=PORT, debug=True)
