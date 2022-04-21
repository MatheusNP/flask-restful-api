from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
import sqlite3

def normalize_path_params(
    city = None,
    grade_min = 0,
    grade_max = 5,
    daily_min = 0,
    daily_max = 10000,
    limit = 50,
    offset = 0,
    **data
):
    if city:
        return {
            'grade_min': grade_min,
            'grade_max': grade_max,
            'daily_min': daily_min,
            'daily_max': daily_max,
            'city': city,
            'limit': limit,
            'offset': offset
        }
    return {
        'grade_min': grade_min,
        'grade_max': grade_max,
        'daily_min': daily_min,
        'daily_max': daily_max,
        'limit': limit,
        'offset': offset
    }


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

        if not params.get('city'):
            sql = " SELECT * FROM hotels \
                    WHERE grade BETWEEN ? AND ? \
                    AND daily BETWEEN ? AND ? \
                    LIMIT ? OFFSET ?"
        else:
            sql = " SELECT * FROM hotels \
                    WHERE grade BETWEEN ? AND ? \
                    AND daily BETWEEN ? AND ? \
                    AND city = ? \
                    LIMIT ? OFFSET ?"
        
        params_tupla = tuple([params[key] for key in params])
        result = cursor.execute(sql, params_tupla)

        hotels = []
        for row in result:
            hotels.append({
                'id': row[0],
                'name': row[1],
                'grade': row[2],
                'daily': row[3],
                'city': row[4]
            })

        return {'success': True, 'data': hotels}

class Hotel(Resource):
    form = reqparse.RequestParser()
    form.add_argument('name', type=str, required=True, help="Field 'name' is required.")
    form.add_argument('grade', type=float, required=True, help="Field 'grade' is required.")
    form.add_argument('daily', type=float, required=True, help="Field 'daily' is required.")
    form.add_argument('city', type=str, required=True, help="Field 'city' is required.")


    def get(self, id):
        hotel = HotelModel.find(id)
        if hotel:
            return {'success': True, 'data': hotel.json()}
        return {'success': False, 'message': 'Hotel not found'}, 404


    @jwt_required()
    def post(self, id):
        if HotelModel.find(id):
            return {'success': False, 'data': 'Hotel already exists'}, 409

        data = Hotel.form.parse_args()
        hotel = HotelModel(id, **data)

        try:
            hotel.save()
            return {'success': True, 'data': hotel.json()}, 201
        except:
            return {'success': False, 'message': 'An internal error ocurred trying to save hotel'}, 500


    @jwt_required()
    def put(self, id):
        data = Hotel.form.parse_args()

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
