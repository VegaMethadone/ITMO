import random

A = [0] * 200
for pog in range(len(A)):
    A[pog] = random.randint(1, 200)

print("######################################")
print(A)
print("######################################")

N = len(A)
for pos in range(0, N - 1):
    for i in range(pos + 1, N):
        if A[i] < A[pos]:
            tmp = A[i]
            A[i] = A[pos]
            A[pos] = tmp

print("######################################")
print(A)
print("######################################")
