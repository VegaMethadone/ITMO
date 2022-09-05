x = 0
summ = 0
for i in range(924-1, 9432+1):
    if (i % 7 == 0 and i % 11 != 0 and
            i % 13 != 0 and i % 15 != 0 and i % 24 != 0):
        x = x + 1
        if summ < i:
            summ = i
print(x)
print(summ)
