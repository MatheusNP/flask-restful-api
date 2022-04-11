from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hotels = [
    {
        'id': 'alpha',
        'name': 'Alpha Hotel',
        'grade': 4.3,
        'daily': 540.90,
        'city': 'São Paulo'
    },
    {
        'id': 'bravo',
        'name': 'Bravo Hotel',
        'grade': 3.9,
        'daily': 400.55,
        'city': 'Rio de Janeiro'
    },
    {
        'id': 'charlie',
        'name': 'Charlie Hotel',
        'grade': 4.9,
        'daily': 550.00,
        'city': 'Rio de Janeiro'
    }
]

class Hotels(Resource):
    def get(self):
        return {'success': True, 'data': hotels}

class Hotel(Resource):
    form = reqparse.RequestParser()
    form.add_argument('name')
    form.add_argument('grade')
    form.add_argument('daily')
    form.add_argument('city')

    def find(hotel_id):
        return next((hotel for hotel in hotels if hotel['id'] == hotel_id), None)

    def get(self, id):
        hotel = Hotel.find(id)
        if hotel:
            return {'success': True, 'data': hotel}
        return {'success': False, 'message': 'Hotel not found'}, 404
    
    def post(self, id):
        hotel = Hotel.find(id)
        if hotel:
            return {'success': False, 'data': 'Hotel already exists'}, 409

        data = Hotel.form.parse_args()
        new_hotel = HotelModel(id, **data).json()

        hotels.append(new_hotel)

        return {'success': True, 'data': new_hotel}, 201
    
    def put(self, id):
        data = Hotel.form.parse_args()
        new_hotel = HotelModel(id, **data).json()

        hotel = Hotel.find(id)
        if hotel:
            hotel.update(new_hotel)
            return {'success': True, 'data': hotel}

        hotels.append(new_hotel)

        return {'success': True, 'data': new_hotel}, 201

    def delete(self, id):
        hotel = Hotel.find(id)
        if hotel:
            hotels.remove(hotel)
            return {'success': True}

        return {'success': False, 'message': 'Hotel not found'}, 404

         
