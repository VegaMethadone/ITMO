def f(n):
    if n == 1:
        return 1
    elif  n >= 2:
        return f(n - 1) - 2 * g(n - 1)

def g(n):
    if n ==1:
        return 1
    elif n >= 2:
        return f(n - 1) + g(n - 1) + n

g(36)