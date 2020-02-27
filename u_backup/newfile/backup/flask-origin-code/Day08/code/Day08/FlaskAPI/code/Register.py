import requests

if __name__ == '__main__':

    username = "SB"

    password = "000"

    data = {
        "username": username,
        "password": password,
        "action": "register"
    }

    response = requests.post("http://127.0.0.1:5000/users/", data=data)

    print(response.json())
