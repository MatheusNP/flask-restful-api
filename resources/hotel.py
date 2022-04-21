from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

class Hotels(Resource):
    def get(self):
        return {'success': True, 'data': [hotel.json() for hotel in HotelModel.query.all()]}

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
