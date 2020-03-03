import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

DATABASE = {
    'ENGINE': "mysql",
    'DRIVER': 'pymysql',
    'HOST': 'localhost',
    'PORT': 3306,
    'USER': 'root',
    'PASSWORD': '000000',
    'NAME': 'HelloTornado'
}
