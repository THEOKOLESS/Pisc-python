def my_var():
    a = 42
    b = "42"
    c = "quarante-deux"
    d = 42.0
    e = True
    f = [42]
    g = {42:42}
    h = (42,)
    i = set()
    print("42 has a type", type(a))
    print("42 has a type", type(b))
    print("quarante-deux has a type", type(c))
    print("42.0 has a type", type(d))
    print("True has a type", type(e))
    print("[42] has a type", type(f))
    print("{42:42} has a type", type(g))
    print("(42,) has a type", type(h))
    print("set() has a type", type(i))

if __name__ == '__main__':
    my_var()