

class Person():

    name = "666"

    age = 77

    def eat(self, food="苹果"):
        print("我喜欢吃吃吃%s" % food)


def drink():
    print("呵呵呵")


if __name__ == '__main__':
    p = Person()

    age = getattr(p, "age", None)

    print(age)

    hobby = getattr(p, "hobby", None)

    print(hobby)

    eat = getattr(p, "eat", None)

    print(eat)

    if eat:
        eat(food="垃圾")

    d = drink

    print(d)

    d()

