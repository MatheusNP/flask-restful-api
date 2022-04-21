from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.site import SiteModel

form = reqparse.RequestParser()
form.add_argument('name', type=str, required=True, help="Field 'name' is required")
form.add_argument('url', type=str, required=True, help="Field 'url' is required")

class Sites(Resource):
    def get(self):
        return {'success': True, 'data': [site.json() for site in SiteModel.query.all()]}


    @jwt_required()
    def post(self):
        data = form.parse_args()

        if SiteModel.find_by_url(data['url']):
            return {'success': False, 'message': "Site '{}' already exists".format(data['url'])}, 400

        site = SiteModel(**data)
        try:
            site.save()
            return {'success': True, 'data': site.json()}
        except:
            return {'success': False, 'message': "An internal error ocurred trying to create a new site"}, 500

class Site(Resource):
    def get(self, id):
        site = SiteModel.find(id)
        if site:
            return {'success': True, 'data': site.json()}
        return {'success': False, 'message': "Site not found"}, 404


    @jwt_required()
    def delete(self, id):
        site = SiteModel.find(id)
        if site:
            try:
                site.delete()
                return {'success': True}
            except:
                return {'success': False, 'message': 'An internal error ocurred trying to delete site'}, 500

        return {'success': False, 'message': "Site not found"}, 404
