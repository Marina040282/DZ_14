from typing import Optional

from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from werkzeug.exceptions import NotFound
from project.dao.base import BaseDAO
from project.models import Movie


class MovieDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_by_filter(self, status: Optional[str], page: Optional[int] = None) -> list[Movie]:
        stmt: BaseQuery = self._db_session.qvery(self.__model__)
        if status == 'new':
            stmt = stmt.order_by(desc(self.__model__.year))
        else:
            stmt = stmt.order_by(self.__model__.year)
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()
