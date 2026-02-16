def g(f,n):
    if n == 0:
        return f() + " 0"
    if type(f) == str:
        return f
    return f() + " " + g(f,n-1)


def f():
    return "f"

print(g(g(f,2),3))