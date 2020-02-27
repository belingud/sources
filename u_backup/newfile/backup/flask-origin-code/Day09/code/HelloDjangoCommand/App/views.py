import random

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from App.models import Grade, Student


def index(request):
    # return render(request, "App/index.html")

    template = loader.get_template("App/index.html")

    return HttpResponse(template.render())


def add_grade(request):

    grade = Grade()

    grade.g_name = "Python19%d" % random.randrange(1000)

    grade.save()

    return HttpResponse("添加成功%s" % grade.g_name)


def get_grades(request):

    grades = Grade.objects.all()

    return render(request, "App/GradeList.html", context={"grades": grades})


def add_student(request):

    student = Student()
    student.s_name = "小明%d" % random.randrange(100)
    student.s_age = random.randrange(100)

    grades = list(Grade.objects.all())

    # 随机取出一个班级
    grade = random.choice(grades)

    student.s_grade = grade

    student.save()

    return HttpResponse("添加成功%s" % student.s_name)


def get_grade(request):

    # 接收班级id
    grade_id = request.GET.get("grade_id")

    grade = Grade.objects.get(pk=grade_id)

    return render(request, "App/Grade.html", context={"grade": grade})
