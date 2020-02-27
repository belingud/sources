import random


def bug(params=[]):

    # if params is None:
    #     params = []

    a = random.randrange(100)

    print(a)

    params.append(a)

    b = random.randrange(200)

    print(b)

    params.append(b)

    print(params)


bug()

print("bug1")

bug()

bug()
bug()
bug()
bug()
