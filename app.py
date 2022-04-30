from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hotels, Hotel
from resources.site import Sites, Site
from resources.user import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from sql_alchemy import database
from settings import CONFIG

app = Flask(__name__)

for key, value in CONFIG.items():
    app.config[key] = value

database.init_app(app)

api = Api(app)
jwt = JWTManager(app)

@app.route('/')
def index():
    return "<h1>Bem vindo ao PyVago!</h1>"

@app.before_first_request
def connect():
    database.create_all()

@jwt.token_in_blocklist_loader
def verify_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def revoked_token(jwt_header, jwt_payload):
    return jsonify({'success': False, 'message': "You have been logged out"}), 401

@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return jsonify({'success': False, 'message': "Your token has expired"}), 401

api.add_resource(Hotels, '/hotels')
api.add_resource(Hotel, '/hotels/<int:id>')
api.add_resource(User, '/user')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<int:id>')