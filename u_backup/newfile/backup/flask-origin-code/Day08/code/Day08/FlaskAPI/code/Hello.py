

class User():

    def __init__(self, username, password):
        self.username = username
        self._password = password

    # 密码是不可被访问
    @property
    def password(self):
        # 调用
        # return self._password
        raise Exception("can't be access")

    @password.setter
    def password(self, password):
        self._password = password

    def check_password(self, password):
        return self._password == password


if __name__ == '__main__':
    user = User("Rock", 110)

    user.password = 120
    # print(user.password)
    print(user.check_password(110))

    print(user.password)