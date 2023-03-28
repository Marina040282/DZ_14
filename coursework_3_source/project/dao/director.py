from project.dao.base import BaseDAO
from project.models import Director


class DirectorDAO(BaseDAO[Director]):
    __model__ = Director
