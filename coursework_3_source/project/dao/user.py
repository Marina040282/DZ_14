from sqlalchemy.exc import IntegrityError

from project.exceptions import UserAlreadyExists
from project.tools.security import generate_password_hash
from project.models import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def get_by_password(self, password):
        return self.session.query(User).filter(User.password == password).first()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        try:
            ent = User(**user_d)
            self.session.add(ent)
            self.session.commit()
        except IntegrityError:
            raise UserAlreadyExists
        return ent

    def delete(self, rid):
        user = self.get_one(rid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        if user_d.get("email"):
            user.email = user_d.get("email")
        if user_d.get("password"):
            user.password = user_d.get("password")
        if user_d.get("name"):
            user.name = user_d.get("name")
        if user_d.get("surname"):
            user.surname = user_d.get("surname")
        # if user_d.get("favorite_genre"):
        # user.favorite_genre = user_d.get("favorite_genre")
        try:
            self.session.add(user)
            self.session.commit()
        except IntegrityError:
            raise UserAlreadyExists

    def update_password(self, email, new_password):
        user = self.get_by_email(email)
        user.password = generate_password_hash(new_password)
        self.session.add(user)
        self.session.commit()

    def update_new_password(self, password, new_password):
        user = self.get_by_password(password)
        user.password = generate_password_hash(new_password)
        self.session.add(user)
        self.session.commit()
