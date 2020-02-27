from flask import request
from flask_restful import Resource, marshal_with, fields, marshal
from .models import Book

book_fields = {
    "b_name": fields.String,
    "b_price": fields.Float,
    "id": fields.Integer,
    "b_author": fields.String
}


class BooksResource(Resource):

    def get(self):

        books = Book.query.all()

        data = {
            "status": 200,
            "msg": "ok",
            "data": [book.to_dict() for book in books]
        }

        return data

    @marshal_with(book_fields)
    def post(self):
        b_name = request.form.get("b_name")
        b_price = request.form.get("b_price")
        book = Book(b_name=b_name, b_price=b_price)

        if not book.save():

            data = {
                "msg": "save fail",
                "status": 400
            }

            return data

        data = {
            "msg": "save success",
            "status": 201,
            # 格式化数据     ①数据 ②模板
            "data": marshal(book, book_fields)
        }

        return data
        # return marshal(book, book_fields)
