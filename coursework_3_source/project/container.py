from project.dao import DirectorDAO
from project.dao import MovieDAO
from project.dao import UserDAO
from project.dao import GenresDAO

from project.services import DirectorsService
from project.services import AuthService
from project.services import MoviesService
from project.services import UserService
from project.services import GenresService
from project.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)
director_dao = DirectorDAO(db.session)
user_dao = UserDAO(db.session)
movie_dao = MovieDAO(db.session)
auth_dao = UserDAO(db.session)

# Services
director_service = DirectorsService(dao=director_dao)
movie_service = MoviesService(dao=movie_dao)
user_service = UserService(dao=user_dao)
genre_service = GenresService(dao=genre_dao)
auth_service = AuthService(user_service)
