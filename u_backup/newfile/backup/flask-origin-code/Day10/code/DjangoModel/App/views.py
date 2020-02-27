from django.db.models import Avg, Max, F, Q
from django.http import HttpResponse
from django.shortcuts import render

from App.models import Game, Book, Praise, Grade, Student


def get_games(request):
    # Flask写法
    # games = Game.objects.filter(Game.g_price.__gt__(50))

    # games = Game.objects.filter(g_price__gt=50).filter(g_price__lt=80)
    games = Game.objects.exclude(g_price__gt=50).order_by("g_id")

    count = games.count()

    print(count)

    if games.exists():
        print("存在数据")

    msg = "hehe"

    print(games)
    print(games.values())
    print(list(games.values()))

    # print(games[0:1])

    # 第一个数字 相当于跳过前多少条  offset   第二个数字，取到第多少条，   实际条数  第二个减去第一个（最多）  limit
    games = games[2:4]

    return render(request, "GameList.html", context=locals())


def add_game(request):

    # game = Game.objects.create(g_name="SL", g_price=100)
    game = Game.create()

    return HttpResponse("游戏添加成功 %d" % game.g_id)


def get_game(request):

    game = Game.objects.get(g_id__gt=3)

    print(game)

    return HttpResponse("获取成功")


def add_books(request):

    for i in range(100):
        Book.objects.create(b_name="CookBook%d" % i)

    return HttpResponse("创建成功")


def get_books(request):

    # page = int(request.GET.get("page") or 1)
    #
    # per_page = int(request.GET.get("per_page") or 10)

    # 值① offset  值②减去值①就是 limit

    # books = Book.objects.all()[(page-1)*per_page:page*per_page]

    # books = Book.objects.filter(b_name__contains="1")
    # books = Book.objects.filter(b_name__endswith="1")
    # books = Book.objects.filter(b_name__istartswith="cook")

    # pk 主键
    # books = Book.objects.filter(pk__in=[1,2,3])
    books = Book.objects.filter(b_publish_date__year=2020)

    return render(request, "BookList.html", context=locals())


def get_praise(request):

    praise = Praise.objects.order_by("id").first()

    # praise = Praise()

    book = praise.p_book

    print(book)
    # 自动生成级联属性 并且携带id
    book_id = praise.p_book_id

    print(book_id)

    return HttpResponse("级联数据")


def get_grades(request):

    # grades = Grade.objects.filter(student__s_name="小明")
    # grades = Grade.objects.filter(g_girl_nums__gt=F("g_boy_nums")+65)

    # grades = Grade.objects.filter(g_girl_nums__gt=3)
    # grades = Grade.objects.filter(~Q(g_girl_nums__gt=3))
    # grades = Grade.objects.exclude(g_girl_nums__gt=3)
    # grades = Grade.objects.filter(g_girl_nums__lte=3)

    grades = Grade.objects.filter(Q(g_girl_nums__gt=60) & Q(g_boy_nums__gt=80))
    print(grades.query)

    return render(request, "GradeList.html", locals())


def get_age(request):

    # result = Student.objects.aggregate(Avg("s_age"))
    # result = Student.objects.filter(s_grade__id=5).aggregate(Avg("s_age"))

    result = Grade.objects.get(pk=5).student_set.aggregate(Max("s_age"))

    print(result)

    return HttpResponse("获取成功")