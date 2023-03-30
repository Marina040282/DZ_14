from flask_restx import Namespace, Resource
from flask import request

from project.container import user_service
from project.setup.api.models import user

user_ns = Namespace('user')


@user_ns.route('/<int:user_id>/')
class UserView(Resource):
    @user_ns.response(404, 'Not Found')
    @user_ns.marshal_with(user, code=200, description='OK')
    def get(self, user_id: int):
        """
        Get user by id.
        """
        return user_service.get_one(user_id)

    def patch(self, user_id):
        data = request.json
        data["id"] = user_id
        user_service.update(data)
        return "", 204


@user_ns.route('/<int:user_id>/password/')
class UserPassword(Resource):
    def put(self, user_id):
        """
        Oбновить пароль пользователя
        """
        user = user_service.get_one(user_id)
        password = user.password
        req_json = request.json
        new_password = req_json.get("password", None)
        if new_password is None:
            return "", 400
        user_service.update_new_password(password, new_password)
        return "", 200
