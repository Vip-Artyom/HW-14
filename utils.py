import sqlite3  # Импортируем библиотеку SQL
from flask import jsonify

def get_sql_connecting(query):
    '''Подключаем базу данных SQL'''
    connect = sqlite3.connect("netflix.db")
    cursor = connect.cursor()
    cursor.execute(query)
    executed_query = cursor.fetchall()
    connect.close()
    return executed_query


def search_for_title(find_title):
    '''Функция ищет фильм по названию'''
    sqlite_query = f"""
        SELECT title, country, MAX(release_year), listed_in, description
        FROM netflix
        WHERE title LIKE "%{find_title}%"
        """  # код запроса
    result_for_query = get_sql_connecting(sqlite_query)

    result = {}
    for content in result_for_query:
        result['title'] = content[0]
        result['country'] = content[1]
        result['release_year'] = content[2]
        result['genre'] = content[3]
        result['description'] = content[4].strip()

    return result


def search_for_year(year_1, year_2):
    '''Функция находит фильмы в диапазоне годов'''

    sqlite_query = (f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {year_1} AND {year_2}
            LIMIT 100            
            """)  # код запроса
    result_for_query = get_sql_connecting(sqlite_query)

    result_list = []
    for content in result_for_query:
        result = {}
        result['title'] = content[0]
        result['release_year'] = content[1]
        result_list.append(result)
    return result_list





def search_for_rating(rating):
    '''Функция находит фильмы по рейтингу'''

    levels = {'children': ["G"], 'family': ["G", "PG", "PG-13"], 'adult': ["R", "NC-17"]}
    if rating in levels:
        level = '\", \"'.join(levels[rating])
        level = f'\"{level}\"'
    else:
        return jsonify([])

    sqlite_query = (f"""
                SELECT title, rating, description
                FROM netflix
                WHERE rating IN ({level})                     
                """)  # код запроса
    result_for_query = get_sql_connecting(sqlite_query)

    result_list = []
    for content in result_for_query:
        result = {}
        result['title'] = content[0]
        result['rating'] = content[1]
        result['description'] = content[2].strip()
        result_list.append(result)

    return result_list


def search_for_genre(genre):
    '''Функция находит фильмы по жанру'''
    sqlite_query = (f"""
                    SELECT title, description
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%'
                    ORDER BY release_year DESC
                    LIMIT 10                  
                    """)  # код запроса
    result_for_query = get_sql_connecting(sqlite_query)

    result_list = []
    for content in result_for_query:
        result = {}
        result['title'] = content[0]
        result['description'] = content[1].strip()
        result_list.append(result)
    return result_list


def repeat_actors(actor_1='Jack Black', actor_2='Dustin Hoffman'):
    '''Функция, которая получает в качестве аргумента имена двух актеров'''
    sqlite_query = (f"""
                        SELECT "cast"
                        FROM netflix
                        WHERE "cast" LIKE '%{actor_1}%'
                        AND "cast" LIKE '%{actor_2}%'                
                        """)  # код запроса
    result_for_query = get_sql_connecting(sqlite_query)

    actors = []
    for actor in result_for_query:
        actors.extend(actor[0].split(', '))
    result = []
    for actor in actors:
        if actor not in [actor_1, actor_2]:
            if actors.count(actor) > 2:
                result.append(actor)
    result = set(result)

    return result


def search_for_arg(type_film, release_year, genre):
    '''Функция, с помощью которой можно будет передавать тип картины (фильм или сериал),
    год выпуска и ее жанр, на выходе список фильмов'''
    sqlite_query = (f"""
                            SELECT title, description
                            FROM netflix
                            WHERE "type" = '{type_film}'
                            AND release_year = {release_year}
                            AND listed_in LIKE '%{genre}%'                                         
                            """)  # код запроса
    result_for_query = get_sql_connecting(sqlite_query)

    result_list = []
    for content in result_for_query:
        result_list.append({
        'title': content[0],
        'description': content[1].strip()
        })

    return result_list

