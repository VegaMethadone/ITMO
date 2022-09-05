x = 0
summ = 0
for i in range(1043, 7237+1):
    if (i % 4 == 0) and  (i % 12 != 0) and (i % 16 != 0) and (i % 25 != 0):
        x += 1
        if summ < i:
            summ = i
print(x)
print(summ)