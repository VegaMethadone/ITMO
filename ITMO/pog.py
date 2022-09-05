for i in range(100, 999):
    n = i
    m = 0
    while n > 0:
        d = n % 10
        if d % 3 == 0:
            if d > m:
                m = d
        n = n // 10
    if m == 0:
         print('NO')
    else:
         print(i)