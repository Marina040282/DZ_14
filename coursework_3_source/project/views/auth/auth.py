from flask_restx import Namespace, Resource
from flask import request

from project.container import user_service, auth_service
from project.setup.api.models import auth, auth_result


auth_ns = Namespace('auth')


@auth_ns.route('/register/')
class AuthView(Resource):
    @auth_ns.expect(auth)
    @auth_ns.response(201, description='OK')
    def post(self):
        """
        Регистрация пользователя
        """
        user_service.create(request.json)
        return 'OK', 201


@auth_ns.route('/login/')
class AuthView(Resource):
    @auth_ns.expect(auth)
    @auth_ns.response(auth_result, code=200)
    def post(self):
        """
        Аутентификация пользователя
        """
        data = request.json
        email = data.get("email", None)
        password = data.get("password", None)
        if None in [email, password]:
            return "", 400

        tokens = auth_service.generate_tokens(email, password)
        return tokens, 200

    def put(self):
        """
        Создание новой пары токенов
        """
        data = request.json
        token = data.get("refresh_token")
        tokens = auth_service.approve_refresh_token(token)
        return tokens, 200