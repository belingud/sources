import json

import pymysql


def read_banners():

    images = []

    with open("getBanner.json") as banners_file:
        banners_json = banners_file.read()
        # print(banners_json)
        banners_data = json.loads(banners_json).get("data")

        # print(banners_data)

        for banner in banners_data:
            image = banner.get("image")
            images.append(image)

    return images


def insert_db(images):
    mysql_client = pymysql.Connect(host="localhost", port=3306, user="root", password="000000", charset="utf8", database="FlaskWork")

    mysql_client.begin()

    cursor = mysql_client.cursor()

    for image in images:

        cursor.execute('INSERT INTO banner(image) VALUES ("%s");' % image)

    mysql_client.commit()


if __name__ == '__main__':
    images = read_banners()
    print(images)

    insert_db(images)
