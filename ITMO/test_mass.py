import random

A = [0] * 200
for kek in range(len(A)):
    A[kek] = random.randint(1, 200)
    
bypass = 0
N = len(A)
for bypass in range(1, N):
    for i in range(N - bypass):
        if A[i] > A[i + 1]:
            tmp = A[i]
            A[i] = A[i + 1]
            A[i + 1] = tmp
bypass += 1

print(A)
