import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import table_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)


#Создание таблицы User
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(25))
    role = db.Column(db.String(10))
    phone = db.Column(db.String(25))

    def tu_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


#Создание таблицы Order
class Order(db.Model):
    __tablename__ = 'Order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def tu_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


#Создание таблицы Offer
class Offer(db.Model):
    __tablename__ = 'Offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def tu_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


#Добавление данных из файла в БД
with app.app_context():
    db.create_all()

    for user_data in table_data.users:
        db.session.add(User(**user_data))

    for order_data in table_data.orders:
        order_data['start_date'] = datetime.strptime(order_data['start_date'], '%m/%d/%Y').date()
        order_data['end_date'] = datetime.strptime(order_data['end_date'], '%m/%d/%Y').date()
        db.session.add(Order(**order_data))

    for offer_data in table_data.offers:
        db.session.add(Offer(**offer_data))

    db.session.commit()

#Получение/добавление данных таблицы User
@app.route("/users", methods=['GET', 'POST'])
def get_all_users():
    if request.method == 'GET':
        users = User.query.all()
        result = [user.tu_dict() for user in users]
        return jsonify(result), 200
    elif request.method == 'POST':
        user_data = json.loads(request.data)
        db.session.add(User(**user_data))
        db.session.commit()
        return jsonify(user_data), 201


# Получение данных пользователя по id, удаление и изменение пользователя
@app.route("/users/<int:gid>", methods=['GET', 'PUT', 'DELETE'])
def get_one_user(gid: int):
    user = User.query.get(gid)
    if request.method == 'GET':
        result = user.tu_dict()
        return jsonify(result), 200
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify(""), 204
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user.first_name = user_data.get("first_name")
        user.last_name = user_data.get("last_name")
        user.age = user_data.get("age")
        user.email = user_data.get("email")
        user.role = user_data.get("role")
        user.phone = user_data.get("phone")
        db.session.add(user)
        db.session.commit()
        return jsonify(''), 204


#Получение/добавление данных таблицы Order
@app.route("/orders", methods=['GET', 'POST'])
def get_all_orders():
    if request.method == 'GET':
        orders = Order.query.all()
        result = [order.tu_dict() for order in orders]
        return jsonify(result), 200
    elif request.method == 'POST':
        order_data = json.loads(request.data)
        db.session.add(Order(**order_data))
        db.session.commit()
        return jsonify(order_data), 201


# Получение данных по ордерам по id, удаление и изменение ордеров
@app.route("/orders/<int:gid>", methods=['GET', 'PUT', 'DELETE'])
def get_one_order(gid: int):
    order = Order.query.get(gid)
    if request.method == 'GET':
        result = order.tu_dict()
        return jsonify(result), 200
    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return jsonify(""), 204
    elif request.method == 'PUT':
        order_data = request.json
        order.name = order_data.get("name")
        order.description = order_data.get("description")
        order.start_date = order_data.get("start_date")
        order.end_date = order_data.get("end_date")
        order.address = order_data.get("address")
        order.price = order_data.get("price")
        order.customer_id = order_data.get("customer_id")
        order.executor_id = order_data.get("executor_id")
        db.session.add(order)
        db.session.commit()
        return jsonify(''), 204


#Получение/добавление данных таблицы Offer
@app.route("/offers", methods=['GET', 'POST'])
def get_all_offers():
    if request.method == 'GET':
        offers = Offer.query.all()
        result = [offer.tu_dict() for offer in offers]
        return jsonify(result), 200
    elif request.method == 'POST':
        offer_data = json.loads(request.data)
        db.session.add(Offer(**offer_data))
        db.session.commit()
        return jsonify(offer_data), 201


# Получение данных Offer по id, удаление и изменение Offer
@app.route("/offers/<int:gid>", methods=['GET', 'PUT', 'DELETE'])
def get_one_offer(gid: int):
    offer = Offer.query.get(gid)
    if request.method == 'GET':
        result = offer.tu_dict()
        return jsonify(result), 200
    elif request.method == 'DELETE':
        db.session.delete(offer)
        db.session.commit()
        return jsonify(""), 204
    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer.order_id = offer_data.get("order_id")
        offer.order_id = offer_data.get("order_id")
        db.session.add(offer)
        db.session.commit()
        return jsonify(''), 204


if __name__ == '__main__':
    app.run()
