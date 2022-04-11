from flask import Flask
from flask_restful import Api
from resources.hotel import Hotels, Hotel

app = Flask(__name__)
api = Api(app)

api.add_resource(Hotels, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:id>')

if __name__ == '__main__':
    app.run(debug=True)