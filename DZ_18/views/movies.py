from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from implemented import movie_service

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        year = request.args.get('year')
        filters = {'director_id': director_id,
                   'genre_id': genre_id,
                   'year': year
                   }
        movies = movie_service.get_all(filters)
        return MovieSchema(many=True).dump(movies), 200

    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    def get(self, bid):
        movie = movie_service.get_one(bid)
        return MovieSchema().dump(movie), 200

    def put(self, bid):
        req_json = request.json
        req_json["id"] = bid
        movie_service.update(req_json)
        return "", 204

    def delete(self, bid):
        movie_service.delete(bid)
        return "", 204

    def patch(self, bid):
        req_json = request.json
        req_json["id"] = bid
        movie_service.partially_update(req_json)
        return "", 204
