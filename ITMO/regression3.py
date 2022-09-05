x = 0
summ = 0
for i in range(1033, 7737):
    if (i % 5 == 0) and (i % 11 != 0) and (i % 17 != 0) and (i % 19 != 0) and (i % 23 != 0):
        x += 1
        if summ < i:
            summ = i
            print(x)
            print(summ)