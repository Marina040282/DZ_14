import calendar
import datetime

import jwt

from constants import JWT_SECRET, JWT_ALGORITHM
from services.users_service import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, email, password, is_refresh=False):
        user = self.user_service.get_by_email(email)

        if user is None:
            raise Exception()

        if not is_refresh:
            if not self.user_service.update_password(user.email, password):
                raise Exception()

        data = {
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "favorite_genre": user.favorite_genre
        }

        # 30 min access_token живет
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        # 130 days refresh_token живет
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return {"access_token": access_token, "refresh_token": refresh_token}

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = data.get("email")

        user = self.user_service.get_by_email(email=email)

        if user is None:
            raise Exception()
        return self.generate_tokens(email, user.password, is_refresh=True)
