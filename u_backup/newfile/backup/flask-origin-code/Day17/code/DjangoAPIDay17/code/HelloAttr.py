

class Person():

    def eat(self):
        print("你就会吃")

    def sleep(self):
        print("我不仅会吃，还能睡")


if __name__ == '__main__':
    actions = {
        "get": "eat",
        "post": "sleep"
    }

    p = Person()

    for method, action in actions.items():
        handler = getattr(p,action)
        print(action, handler)
        setattr(p, method, handler)

    # p.eat()
    p.post()