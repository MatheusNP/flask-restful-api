from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from resources.helpers.filters import normalize_path_params, sql_wout_city, sql_with_city
import sqlite3


form = reqparse.RequestParser()
form.add_argument('name', type=str, required=True, help="Field 'name' is required.")
form.add_argument('grade', type=float, required=True, help="Field 'grade' is required.")
form.add_argument('daily', type=float, required=True, help="Field 'daily' is required.")
form.add_argument('city', type=str, required=True, help="Field 'city' is required.")
form.add_argument('site_id', type=int, required=True, help="Field 'site_id' is required.")

path_params = reqparse.RequestParser()
path_params.add_argument('city', type=str)
path_params.add_argument('grade_min', type=float)
path_params.add_argument('grade_max', type=float)
path_params.add_argument('daily_min', type=float)
path_params.add_argument('daily_max', type=float)
path_params.add_argument('limit', type=int)
path_params.add_argument('offset', type=int)

class Hotels(Resource):

    def get(self):
        connection = sqlite3.connect('pyvago.db')
        cursor = connection.cursor()

        data = path_params.parse_args()
        data_valid = {key: data[key] for key in data if data[key] is not None}
        params = normalize_path_params(**data_valid)

        sql = sql_wout_city
        if params.get('city'):
            sql = sql_with_city

        params_tupla = tuple([params[key] for key in params])
        result = cursor.execute(sql, params_tupla)

        hotels = []
        for row in result:
            hotels.append({
                'id': row[0],
                'name': row[1],
                'grade': row[2],
                'daily': row[3],
                'city': row[4],
                'site_id': row[5],
            })

        return {'success': True, 'data': hotels}


    @jwt_required()
    def post(self):
        data = form.parse_args()

        if HotelModel.findByName(data['name']):
            return {'success': False, 'data': 'Hotel already exists'}, 409

        if not SiteModel.find(data['site_id']):
            return {'success': False, 'data': 'Site not exists'}, 409

        hotel = HotelModel(**data)

        try:
            hotel.save()
            return {'success': True, 'data': hotel.json()}, 201
        except:
            return {'success': False, 'message': 'An internal error ocurred trying to save hotel'}, 500

class Hotel(Resource):

    def get(self, id):
        hotel = HotelModel.find(id)
        if hotel:
            return {'success': True, 'data': hotel.json()}
        return {'success': False, 'message': 'Hotel not found'}, 404


    @jwt_required()
    def put(self, id):
        data = form.parse_args()

        if HotelModel.findByName(data['name']) and HotelModel.findByName(data['name']).id is not id:
            return {'success': False, 'data': 'Hotel already exists'}, 409

        if not SiteModel.find(data['site_id']):
            return {'success': False, 'data': 'Site not exists'}, 409

        hotel = HotelModel.find(id)
        if hotel:
            hotel.update(**data)
            try:
                hotel.save()
                return {'success': True, 'data': hotel.json()}
            except:
                return {'success': False, 'message': 'An internal error ocurred trying to save hotel'}, 500

        new_hotel = HotelModel(id, **data)
        try:
            new_hotel.save()
            return {'success': True, 'data': new_hotel.json()}, 201
        except:
            return {'success': False, 'message': 'An internal error ocurred trying to save hotel'}, 500


    @jwt_required()
    def delete(self, id):
        hotel = HotelModel.find(id)
        if hotel:
            try:
                hotel.delete()
                return {'success': True}
            except:
                return {'success': False, 'message': 'An internal error ocurred trying to delete hotel'}, 500

        return {'success': False, 'message': 'Hotel not found'}, 404
