from project.dao.user import UserDAO
from project.tools.security import generate_password_hash


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def get_by_email(self, email):
        return self.dao.get_by_email(email)

    def create(self, user_d):
        user_d["password"] = generate_password_hash(user_d[("password")])
        return self.dao.create(user_d)

    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao

    def update_password(self, password, new_password):
        self.update_password(password, new_password)

    def delete(self, rid):
        self.dao.delete(rid)
