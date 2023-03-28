from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режисер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Стив Энтин'),
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'trailer': fields.String(required=True),
    'year': fields.Integer(required=True),
    'rating': fields.Float(required=True),
    'genre_id': fields.Integer(required=True),
    'director_id': fields.Integer(required=True),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director),
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'name': fields.String(),
    'surname': fields.String(),
    'favorite_genre': fields.Integer(),
    'genre': fields.Nested(genre),
})

auth: Model = api.model('Авторизация', {
    'email': fields.String(required=True, example='Marina0282@gmail.com'),
    'password': fields.String(required=True, example='qwerty'),
})

auth_result: Model = api.model('', {
    'access_token': fields.String(required=True),
    'refresh_token': fields.String(required=True),
})
