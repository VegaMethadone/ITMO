import random

A = [0] * 200
for kek in range(len(A)):
    A[kek] = random.randint(1, 200)

is_sorted = False
bypass = 0
while not is_sorted:
    bypass += 1
    numm = 0
    N = len(A)
    is_sorted = True
    for i in range(N - bypass):
        if A[i] > A[i + 1]:
            tmp = A[i]
            A[i] = A[i + 1]
            A[i + 1] = tmp
            is_sorted = False
        numm += 1
    print(f"Number is: {numm}. Massive is: {A}")

