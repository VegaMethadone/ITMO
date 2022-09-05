import random

A = [0] * 200
for pog in range(len(A)):
    A[pog] = random.randint(1, 200)

N = len(A)

F = [0] * N
for x in A:
    F[x] += 1

for x in range(0, N):
    for k in range(F[x]):
        print(x)
