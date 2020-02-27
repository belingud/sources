import requests


def send():

    response = requests.get("http://127.0.0.1:5000")

    print(response.json())


if __name__ == '__main__':
    send()