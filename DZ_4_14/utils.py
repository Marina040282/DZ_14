import sqlite3


def get_all(query: str):
    """ Функция получает данные с БД и выводит список всех сторок """
    with sqlite3.connect('netflix.db') as conn:
        conn.row_factory = sqlite3.Row

        result = []

        for item in conn.execute(query).fetchall():
            result.append(dict(item))

        return result


def get_one(query: str):
    """ Функция получает данные с БД и одну строку или None, если по запросу она не была найдена """
    with sqlite3.connect('netflix.db') as conn:
        conn.row_factory = sqlite3.Row

        result = conn.execute(query).fetchone()

        if result is None:
            return None
        else:
            return dict(result)


def by_cast(name1: str = 'Ben Lamb', name2: str = 'Rose McIver'):
    """Функция получает в качестве аргумента имена двух актеров,
    сохраняет всех актеров из колонки cast и возвращает список тех,
    кто играет с ними в паре больше 2 раз"""

    sqlite_query = f"""
    SELECT * FROM netflix
    WHERE netflix."cast" LIKE '%{name1}%'
    AND netflix."cast" LIKE '%{name2}%'
    """
    cast = []
    set_cast = set()
    result = get_all(sqlite_query)

    for item in result:
        for actor in item['cast'].split(','):
            cast.append(actor)

    for actor in cast:
        if cast.count(actor) > 2:
            set_cast.add(actor)

    return list(set_cast)


def get_movie_by_genre(year: str = '2018', genre: str = 'Comedies', type: str = 'Movie'):
    """  Функция с помощью которой можно будет передавать тип картины (фильм или сериал),
    год выпуска и ее жанр и получать на выходе список названий картин с их описаниями в JSON"""

    sqlite_query = f"""
    SELECT title, description  FROM netflix
    WHERE release_year = '{year}'
    AND listed_in LIKE '%{genre}%'
    AND type = '{type}'
    """
    result = []
    for item in get_all(sqlite_query):
        result.append(
            {
                'title': item['title'],
                'description': item['description'],
            }
        )
    return result
