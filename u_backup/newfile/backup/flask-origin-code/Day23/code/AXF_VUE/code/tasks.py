from time import sleep

from celery import Celery

app = Celery("tasks", broker="redis://:rock1204@localhost:6379/1")


@app.task
def send_mail():

    sleep(5)

    return "发送成功"


if __name__ == '__main__':
    result = send_mail.delay()
    print(result)