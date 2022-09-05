import random

A = [0] * 50
for pog in range(len(A)):
    A[pog] = random.randint(1, 50)

print(A)

N = len(A)
for pos in range(1, N):
    i = pos
    while i > 0 and A[i - 1] > A[i]:
        A[i], A[i - 1] = A[i - 1], A[i]
        i -= 1

print(A)
