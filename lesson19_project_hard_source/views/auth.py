from flask import request
from flask_restx import Resource, Namespace

from implemented import auth_service

auth_ns = Namespace('auth')



@auth_ns.route('/')
class AuthsView(Resource):
    # POST /auth — получает логин и пароль из Body запроса в виде JSON, далее проверяет
    # соотвествие с данными в БД (есть ли такой пользователь, такой ли у него пароль) и если
    # всё оk — генерит пару access_token и refresh_token и отдает их в виде JSON.
    def post(self):
        req_json = request.json
        username = req_json.get("username", None)
        password = req_json.get("password", None)
        if None in [username, password]:
            return "", 401

        tokens = auth_service.generate_tokens(username, password)

        return tokens, 201

    # PUT /auth — получает refresh_token из Body запроса в виде JSON, далее проверяет
    # refresh_token и если он не истек и валиден — генерит пару access_token и refresh_token и
    # отдает их в виде JSON.
    def put(self):
        req_json = request.json
        token = req_json.get("refresh_token")
        tokens = auth_service.approve_refresh_token(token)
        return tokens, 201
