from flask import Flask, jsonify
from utils import get_one, get_all

app = Flask(__name__)


# вьюшка выводит данные про фильм
@app.get('/movie/<title>')
def get_by_title(title: str):
    """ Функция ищет данные по названию и возвращает данные в  формате json"""
    sqlite_query = f"""
    SELECT * FROM netflix 
    WHERE title  = '{title}'  
    ORDER BY date_added desc 
    """

    query_result = get_one(sqlite_query)
    if query_result is None:
        return jsonify(status=404)

    movie = {
        'title': query_result['title'],
        'country': query_result['country'],
        'release_year': query_result['release_year'],
        'genre': query_result['listed_in'],
        'description': query_result['description'],
    }
    return jsonify(movie)


# вьюшка выводит список словарей по заданному диапазону годов выпуска фильмов
@app.get('/movie/<year1>/to/<year2>')
def get_movie_by_year(year1: str, year2: str):
    """ Функция принимает  параметры два года и возвращает данные в  формате json"""
    sqlite_query = f"""
    SELECT * FROM netflix 
    WHERE release_year BETWEEN {year1} AND {year2}
    LIMIT 100 
    """

    result = []

    for item in get_all(sqlite_query):
        result.append(
            {
                'title': item['title'],
                'release_year': item['release_year'],
            }
        )

    return jsonify(result)


# вьюшка выводит список словарей по заданной возврастной категории
@app.get('/movie/rating/<category>')
def get_movie_by_rating(category: str):
    """Функция принимает список допустимых рейтингов и возвращает данные в  формате json"""
    sqlite_query = f"""
    SELECT * FROM netflix
    """
    if category == 'children':
        sqlite_query += ' WHERE rating = "G"'
    elif category == 'family':
        sqlite_query += ' WHERE rating = "G" or rating = "PG" or rating = "PG-13"'
    elif category == 'adult':
        sqlite_query += ' WHERE rating = "R" or rating = "NC-17"'
    else:
        return jsonify(status=400)

    result = []

    for item in get_all(sqlite_query):
        result.append(
            {
                'title': item['title'],
                'rating': item['rating'],
                'description': item['description'],
            }
        )

    return jsonify(result)


# вьюшка выводит список словарей по жанру
@app.get('/genre/<genre>')
def get_movie_by_genre(genre: str):
    """Функция получает название жанра в качестве аргумента и возвращает 10
    самых свежих фильмов в формате json"""
    sqlite_query = f"""
    SELECT * FROM netflix
    WHERE listed_in LIKE '%{genre}%'
    ORDER BY date_added desc
    LIMIT 10
    """

    result = []

    for item in get_all(sqlite_query):
        result.append(
            {
                'title': item['title'],
                'description': item['description'],
            }
        )

    return jsonify(result)


app.run()
