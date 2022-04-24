from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hotels, Hotel
from resources.site import Sites, Site
from resources.user import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from sql_alchemy import database

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pyvago.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTY1MDU1Mjk1NywiaWF0IjoxNjUwNTUyOTU3fQ.OBL4_3RCM-zICx7BSTl1uiQtah_hMEUYYwZjiFKNQ6M"
app.config['JWT_BLACKLIST_ENABLED'] = True

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

api.add_resource(Hotels, '/hotels')
api.add_resource(Hotel, '/hotels/<string:id>')
api.add_resource(User, '/users/<int:id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<int:id>')