import random

A = [0]* 200
for index in range(len(A)):
    A[index] = random.randint(1, 200)

B = [0]* 200
for index in range(len(B)):
    B[index] = random.randint(1, 200)

N = len(A)
for pos in range(1, N):
    i = pos
    while i > 0 and  A[i - 1] > A[i]:
        A[i], A[i - 1] = A[i - 1], A[i]
        i -= 1

for pos in range(1, N):
    i = pos
    while i > 0 and B[i - 1] > B[i]:
        B[i], B[i - 1] = B[i - 1], B[i]
        i -= 1

print(A)
print("######")
print(B)