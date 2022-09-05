import random
A = [0] * 200
for kek in range(200):
    A[kek] = random.randint(1, 200)
print(*A)


N = len(A)
numm = 0
for bypass in range(N - 1):
    for i in range(N - 1):
        if A[i] > A[i + 1]:
            tmp = A[i]
            A[i] = A[i + 1]
            A[i + 1] = tmp
            numm += 1
            print(f"Number: {numm}. Massive: {A}")