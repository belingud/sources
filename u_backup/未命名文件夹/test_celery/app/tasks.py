from celery import shared_task, task
from app.score_celery import app as celery_app


@shared_task
def test_ok():
    print(123)
    return 123
