from setup_db import db
from marshmallow import Schema, fields


# модель Жанр
class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


# схема сериализации Жанр
class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()
