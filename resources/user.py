from datetime import timedelta
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from blacklist import jwt_redis_blacklist
from settings import jwt_ttl_hours

form = reqparse.RequestParser()
form.add_argument('login', type=str, required=True, help="Field 'login' is required")
form.add_argument('password', type=str, required=True, help="Field 'password' is required")

# /user
class User(Resource):
    @jwt_required()
    def get(self):
        user = UserModel.find(get_jwt_identity())
        if user:
            return {'success': True, 'data': user.json()}
        return {'success': False, 'message': "User not found"}, 404


    @jwt_required()
    def delete(self):
        user = UserModel.find(get_jwt_identity())
        if user:
            try:
                user.delete()
                return {'success': True}
            except:
                return {'success': False, 'message': "An internal error ocurred trying to delete user"}, 500

        return {'success': False, 'message': "User not found"}, 404

# /register
class UserRegister(Resource):
    def post(self):
        data = form.parse_args()

        if UserModel.find_by_login(data['login']):
            return {'success': False, 'message': "Login '{}' already exists".format(data['login'])}, 404
        
        user = UserModel(**data)
        try:
            user.save()
            return {'success': True, 'data': user.json()}, 201
        except:
            return {'success': False, 'message': "An internal error ocurred trying to create a new user"}, 500

# /login
class UserLogin(Resource):
    def post(self):
        data = form.parse_args()

        user = UserModel.find_by_login(data['login'])
        if user and safe_str_cmp(user.password, data['password']):
            token = create_access_token(identity=user.id)
            return {'success': True, 'token': token}, 200

        return {'success': False, 'message': "Login or password is incorrect"}, 401


# /logout
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] #JWT Token Indetifier
        jwt_redis_blacklist.set(jwt_id, "", ex=timedelta(hours=jwt_ttl_hours))
        return {'success': True}, 200
