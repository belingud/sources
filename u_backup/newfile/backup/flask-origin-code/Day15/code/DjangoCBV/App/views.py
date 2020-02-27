from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from App.models import Book


def index(request):
    return HttpResponse("Index")


class HelloView(View):

    msg = None

    def get(self, request):
        return HttpResponse("GET OK %s" % self.msg)

    def post(self, request):
        return HttpResponse("POST OK")

    def put(self, request):
        return HttpResponse("PUT OK")


class HelloCustomView(object):

    def dispatch(self, request):

        # return HttpResponse("Dispatch OK")

        # if request.method == "GET":
        #     return self.get(request)
        # elif request.method == "POST":
        #     return self.post(request)
        # elif request.method == "PUT":
        #     return self.put(request)
        # else:
        #     return HttpResponse("请求方法不被支持")

        handler = getattr(self, request.method.lower(), None)
        #
        if not handler:
            return HttpResponse("请求方法不支持")
        #
        return handler(request)

    # @classmethod
    # def as_view(cls):
    #
    #     def view(request):
    #         self = cls()
    #
    #         return self.dispatch(request)
    #     return view

    def get(self, request):
        return HttpResponse("GET OK")

    def post(self, request):
        return HttpResponse("POST OK")

    def put(self, request):
        return HttpResponse("PUT OK")


class HelloTemplateView(TemplateView):

    # template_name = "HelloTemplate.html"
    pass


class HelloListView(ListView):

    model = Book
    # queryset = Book.objects.all()
    # template_name = "BookList.html"


class HelloDetailView(DetailView):
    model = Book
    # queryset = Book.objects.all()
    # query_pk_and_slug = '书名'
    # pk_url_kwarg = 'pk'
    template_name = "bookdetail.html"
    context_object_name = 'Book'
