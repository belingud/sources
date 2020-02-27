from django.shortcuts import render
from app.tasks import test_ok
from django.db.models.signals import post_save
from django.http import JsonResponse
from app.models import Test
# Create your views here.


def test(request):
    # test_ok.delay()
    # from datetime import datetime, timedelta
    # send_date = datetime.utcnow() + timedelta(days=2)
    # test_ok.apply_async(eta=send_date)
    obj = Test.objects.create(name='qwe', password='qwe')
    post_save.send(test, key='value')
    # saved = obj.save()
    print('saved obj: ', obj)
    return JsonResponse({'msg': 'ok'})
