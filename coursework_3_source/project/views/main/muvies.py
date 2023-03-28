from flask_restx import Namespace, Resource
from flask import request

from project.container import movie_service
from project.setup.api.models import movie
from project.setup.api.parsers import status_page_parser

movies_ns = Namespace('movies')


@movies_ns.route('/')
class MoviesView(Resource):
    @movies_ns.expect(status_page_parser)
    @movies_ns.marshal_with(movie, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all movies.
        """
        status = request.args.get('status')
        return movie_service.get_all(filter=status, **status_page_parser.parse_args())


@movies_ns.route('/<int:movie_id>/')
class MovieView(Resource):
    @movies_ns.response(404, 'Not Found')
    @movies_ns.marshal_with(movie, code=200, description='OK')
    def get(self, movie_id: int):
        """
        Get movie by id.
        """
        return movie_service.get_item(movie_id)
