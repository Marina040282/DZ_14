from setup_db import db
from marshmallow import Schema, fields


# модель Режиссер
class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


# схема сериализации Режиссер
class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
