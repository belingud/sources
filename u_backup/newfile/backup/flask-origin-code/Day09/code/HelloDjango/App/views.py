from django.http import HttpResponse
from django.shortcuts import render

from App.models import Book


def index(request):
    return HttpResponse("Index Hello")


def home(request):
    return render(request, "home.html")


def create_book(request):

    book = Book()
    book.b_name = "CookBook"
    book.b_price = 50

    book.save()

    return HttpResponse("创建成功")


def get_book(request):
    books = Book.objects.all()

    print(books)

    return render(request, "books.html",context={"books": books})
