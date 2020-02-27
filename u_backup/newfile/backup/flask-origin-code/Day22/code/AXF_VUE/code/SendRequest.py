import requests

if __name__ == '__main__':
    response = requests.get("http://localhost:8000/home/")

    print(response.json())