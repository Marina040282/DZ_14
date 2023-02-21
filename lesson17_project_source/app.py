# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movie_schema = MovieSchema()
director_schema = DirectorSchema()
genre_schema = GenreSchema()

api = Api(app)
# Создание неймспейcов  с адресами `/movies`, `/directors`, `/genres`
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


# Сlass MoviesView(позволяет
#   с помощью GET-запроса по адресу `/movies` возвращает список всех фильмов, разделенный по страницам
#   с помощью post-запроса добавляет кино в фильмотеку
@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        stnt = Movie.query
        if director_id:
            stnt = stnt.filter(Movie.director_id == director_id)
        if genre_id:
            stnt = stnt.filter(Movie.genre_id == genre_id)
        if director_id and genre_id:
            stnt = stnt.filter(Movie.genre_id == genre_id and Movie.director_id == director_id)
        movies = stnt.all()
        return movie_schema.dump(movies, many=True), 200

    def post(self):
        movie_data = request.json
        db.session.add(Movie(**movie_data))
        db.session.commit()
        return '', 201


# Сlass MovieView(позволяет
#   с помощью GET-запроса по адресу `/movies/<id>` возвращает подробную информацию о фильме
#   с помощью PUT - запроса обновляет кино, DELETE —  удаляет кино
@movie_ns.route('/<int:gid>')
class MovieView(Resource):
    def get(self, gid: int):
        movie = Movie.query.get(gid)
        if not movie:
            return '', 404
        return movie_schema.dump(movie), 200

    def put(self, gid: int):
        movie = Movie.query.get(gid)
        if not movie:
            return '', 404
        movie_data = request.json
        movie.title = movie_data.get('title')
        movie.description = movie_data.get('description')
        movie.trailer = movie_data.get('trailer')
        movie.year = movie_data.get('year')
        movie.rating = movie_data.get('rating')
        movie.genre_id = movie_data.get('genre_id')
        movie.director_id = movie_data.get('director_id')
        db.session.add(movie)
        db.session.commit()
        return '', 204

    def delete(self, gid: int):
        movie = Movie.query.get(gid)
        if not movie:
            return '', 404
        db.session.delete(movie)
        db.session.commit()
        return '', 204


# Сlass DirectorsView(позволяет
#   с помощью GET-запроса по адресу `/directors` возвращает всех режиссеров
#   с помощью post-запроса добавляет режиссера в базу
@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = Director.query.all()
        return director_schema.dump(all_directors, many=True), 200

    def post(self):
        director_data = request.json
        db.session.add(Director(**director_data))
        db.session.commit()
        return '', 201


# Сlass DirectorView(позволяет
#   с помощью GET-запроса по адресу `/directors/<id>` возвращает подробную информацию о режиссере
#   с помощью PUT - запроса обновляет данные о режиссере, DELETE —  удаляет режиссера
@director_ns.route('/<int:gid>')
class DirectorView(Resource):
    def get(self, gid: int):
        director = Director.query.get(gid)
        if not director:
            return '', 404
        return director_schema.dump(director), 200

    def put(self, gid: int):
        director = Director.query.get(gid)
        if not director:
            return '', 404
        director_data = request.json
        director.name = director_data.get('name')
        db.session.add(director)
        db.session.commit()
        return '', 204

    def delete(self, gid: int):
        director = Director.query.get(gid)
        if not director:
            return '', 404
        db.session.delete(director)
        db.session.commit()
        return '', 204


# Сlass GenresView(позволяет
#   с помощью GET-запроса по адресу `/genres` возвращает все жанры
#   с помощью post-запроса добавляет жанр в базу
@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = Genre.query.all()
        return genre_schema.dump(all_genres, many=True), 200

    def post(self):
        genre_data = request.json
        db.session.add(Genre(**genre_data))
        db.session.commit()
        return '', 201


# Сlass GenreView(позволяет
#   с помощью GET-запроса по адресу `/genres/<id>` возвращает информацию о жанре с перечислением списка фильмов по жанру
#   с помощью PUT - запроса обновляет данные о жанре, DELETE —  удаляет жанр
@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        genre = Genre.query.get(gid)
        if not genre:
            return '', 404
        return genre_schema.dump(genre), 200

    def put(self, gid: int):
        genre = Genre.query.get(gid)
        if not genre:
            return '', 404
        genre_data = request.json
        genre.name = genre_data.get('name')
        db.session.add(genre)
        db.session.commit()
        return '', 204

    def delete(self, gid: int):
        genre = Genre.query.get(gid)
        if not genre:
            return '', 404
        db.session.delete(genre)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
