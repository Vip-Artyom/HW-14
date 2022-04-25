from flask import Flask, jsonify
import utils

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/movies/<title>")
def search_movie_for_title(title):
    movie = utils.search_for_title(title)
    return jsonify(movie)


@app.route("/movies/<int:year_1>/to/<int:year_2>")
def search_movie_for_year(year_1, year_2):
    movie = utils.search_for_year(year_1, year_2)
    return jsonify(movie)


@app.route("/rating/<path>/")
def search_movie_for_children(path):

    movie = utils.search_for_rating(path)

    return jsonify(movie)


@app.route("/genre/<genre>")
def search_movie_for_genre(genre):
    movie = utils.search_for_genre(genre)

    return jsonify(movie)


if __name__ == '__main__':
    app.run()
