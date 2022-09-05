x = int(input())
summ = 1
while x != 0:
    d = x % 10
    print(d)
    if d != 0:
        summ *= d
    else: 
        pass
    x = x // 10
print(summ)