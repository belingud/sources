from flask_restful import Api

from Book.views import BooksResource

books_api = Api()

books_api.add_resource(BooksResource, "/books/")
