import sqlite3
import json
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/api/movies', methods=['GET', 'POST'])
def collection():
    if request.method == 'GET':
        all_movies = get_all_movies()
        return json.dumps(all_movies)
    elif request.method == 'POST':
        data = request.form
        result = add_movie(data['lead_actor'], data['title'], data['tagline'])
        return jsonify(result)


@app.route('/api/movie/<movie_id>', methods=['GET', 'PUT', 'DELETE'])
def resource(movie_id):
    if request.method == 'GET':
        movie = get_single_movie(movie_id)
        return json.dumps(movie)
    elif request.method == 'PUT':
        data = request.form
        result = edit_movie(
            movie_id, data['lead_actor'], data['title'], data['tagline'])
        return jsonify(result)
    elif request.method == 'DELETE':
        result = delete_movie(movie_id)
        return jsonify(result)




def add_movie(lead_actor, title, tagline):
    try:
        with sqlite3.connect('movies.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO movies (lead_actor, title, tagline) values (?, ?, ?);
                """, (lead_actor, title, tagline,))
            result = {'status': 1, 'message': 'Movie Added'}
    except:
        result = {'status': 0, 'message': 'error'}
    return result


def get_all_movies():
    with sqlite3.connect('movies.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM movies ORDER BY id desc")
        all_movies = cursor.fetchall()
        return all_movies


def get_single_movie(movie_id):
    with sqlite3.connect('movies.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
        movie = cursor.fetchone()
        return movie


def edit_movie(movie_id, lead_actor, title, tagline):
    try:
        with sqlite3.connect('movies.db') as connection:
            connection.execute("UPDATE movies SET lead_actor = ?, title = ?, tagline = ? WHERE ID = ?;", (lead_actor, title, tagline, movie_id,))
            result = {'status': 1, 'message': 'MOVIE Edited'}
    except:
        result = {'status': 0, 'message': 'Error'}
    return result


def delete_movie(movie_id):
    try:
        with sqlite3.connect('movies.db') as connection:
            connection.execute("DELETE FROM movies WHERE ID = ?;", (movie_id,))
            result = {'status': 1, 'message': 'MOVIE Deleted'}
    except:
        result = {'status': 0, 'message': 'Error'}
    return result


if __name__ == '__main__':
    app.debug = True
    app.run()
