import json

import pymysql


def read_movies():

    with open("getMovies.json") as movies_file:
        movies_json = movies_file.read()
        # print(movies_json)
        movies_data = json.loads(movies_json).get("data")

        # print(movies_data)

        return movies_data


def insert_db(movies):
    mysql_client = pymysql.Connect(host="localhost", port=3306, user="root", password="000000", charset="utf8", database="FlaskWork")

    mysql_client.begin()

    cursor = mysql_client.cursor()

    for movie in movies:

        image = movie.get("image")
        title = movie.get("title")
        duration = movie.get("duration")
        postid = movie.get("postid")

        print(image, title, duration, postid)

        cursor.execute('INSERT INTO movie(image, title, duration, postid) VALUES ("%s", "%s", %d, %d);' %
                       (image, title, int(duration), int(postid)))

    mysql_client.commit()


if __name__ == '__main__':
    movies = read_movies()
    print(movies)

    insert_db(movies)
