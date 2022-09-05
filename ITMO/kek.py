for i in range(10000, 99999):
    x = i
    a = 0
    b = 0
    while x > 0:
        y = x % 10
        if y > 3:
            a = a + 1
        if y < 8:
            b = b + 1
        x = x // 10
    if a == 4 and b == 3:
        print(i)
