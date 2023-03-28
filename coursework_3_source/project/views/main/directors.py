from flask_restx import Namespace, Resource

from project.container import director_service
from project.setup.api.models import director
from project.setup.api.parsers import page_parser

directors_ns = Namespace('directors')


@directors_ns.route('/')
class DirectorsView(Resource):
    @directors_ns.expect(page_parser)
    @directors_ns.marshal_with(director, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all directors.
        """
        return director_service.get_all(**page_parser.parse_args())


@directors_ns.route('/<int:director_id>/')
class DirectorView(Resource):
    @directors_ns.response(404, 'Not Found')
    @directors_ns.marshal_with(director, code=200, description='OK')
    def get(self, director_id: int):
        """
        Get director by id.
        """
        return director_service.get_item(director_id)
