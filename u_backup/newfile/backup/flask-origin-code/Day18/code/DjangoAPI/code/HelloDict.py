

if __name__ == '__main__':

    d = {"name": "Rock", "password": "110", "hobby": "reading"}

    print(d.items())

    for item in d.items():
        print(item)

    l = list("abcd")
    print(l)

    ld = list(d.items())

    print(ld)

    lr = l + ld

    print(lr)
