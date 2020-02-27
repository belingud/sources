from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):

    data = {
        "msg": "VUE",
        "hobby": ["eat", "sleep", "gaming", "study", "reading"],
        "score":{
            "en": 150,
            "ch": 105
        },
        "flag":False
    }

    # return render(request, "Index.html", context=data)
    template = loader.get_template('Index.html')

    result = template.render(context=data)

    print(result)

    return HttpResponse(result)
    # return HttpResponse("<h1>哈哈哈</h1>")
