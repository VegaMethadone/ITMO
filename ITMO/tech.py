import random

A = [0] * 200
for kek in range(len(A)):
    A[kek] = random.randint(1, 200)

N = len(A)
for pos in range(0, N - 1):         #  
    for i in range(pos + 1, N):     # Все, кто правее с позици  POS + 1, если буду пробегать от нуля, то 0 элемент будет всегда выигрывать
        if A[i] < A[pos]:
            tmp = A[i]
            A[i] = A[pos]
            A[pos] = tmp

