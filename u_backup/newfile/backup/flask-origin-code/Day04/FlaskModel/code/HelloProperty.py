import hashlib


class User():

    _password = ""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def password(self):

        print("getter")

        return self._password

    @password.setter
    def password(self, p):

        print("setter")

        hexdigest = hashlib.new("md5", data=str(p).encode("utf-8")).hexdigest()

        self._password = hexdigest


if __name__ == '__main__':

    u = User("Rose", "110")

    print(u.password)
    #
    # u.password = 999
    # #
    # print(u.password)
