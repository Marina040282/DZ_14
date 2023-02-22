from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = director_service.get_all()
        return DirectorSchema(many=True).dump(directors), 200


@director_ns.route('/<int:bid>')
class DirectorView(Resource):
    def get(self, bid):
        director = director_service.get_one(bid)
        return DirectorSchema().dump(director), 200
