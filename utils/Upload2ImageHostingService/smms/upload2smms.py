from logging import log
import os
import requests
LIST_URL = "https://sm.ms/api/list"
UPLOAD_URL = "https://sm.ms/api/upload"
CLEAR_URL = "https://sm.ms/api/clear"


def get_history():
    params = {'ssl': 0, 'format': 'json'}
    r = requests.get(LIST_URL, params)
    print(r.json())


def upload(filepath):
    if not os.path.isfile(filepath):
        print("file not exist")
    smfile = open(filepath, 'rb')
    smfile.close()
    img = {"smfile": open(filepath, 'rb')}
    resp = requests.post(url=UPLOAD_URL, files=img)
    print(resp.json())
    with open('log.txt', 'a') as f:
        for k, v in resp.json()['data'].items():
            f.write(k+':' + str(v) + '\n')
        f.write('###################################\n')


def clear_history():
    r = requests.get(CLEAR_URL)
    print(r.json())
    log(r.json())


upload("./whatsyourproblem.png")

