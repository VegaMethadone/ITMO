x = 0
for i in range(1, 2000):
    d = i
    n = 3
    s = 5
    while s < 2019:
        s += d
        n += 10
    if n == 243:
        x += 1
        print(x)
