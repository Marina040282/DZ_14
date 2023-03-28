from flask_restx import Namespace, Resource

from project.container import genre_service
from project.setup.api.models import genre
from project.setup.api.parsers import page_parser

genres_ns = Namespace('genres')


@genres_ns.route('/')
class GenresView(Resource):
    @genres_ns.expect(page_parser)
    @genres_ns.marshal_with(genre, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all genres.
        """
        return genre_service.get_all(**page_parser.parse_args())


@genres_ns.route('/<int:genre_id>/')
class GenreView(Resource):
    @genres_ns.response(404, 'Not Found')
    @genres_ns.marshal_with(genre, code=200, description='OK')
    def get(self, genre_id: int):
        """
        Get genre by id.
        """
        return genre_service.get_item(genre_id)
