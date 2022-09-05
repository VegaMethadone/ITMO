import random
A = [0] * 200
for kek in range(200):
    A[kek] = random.randint(1, 200)
print(*A)
print("####################################################################")
print("####################################################################")
print("####################################################################")

N = len(A)
i = 0
numm = 0
while i < N - 1:
    if A[i] > A[i + 1]:
        numm += 1
        tmp = A[i]
        A[i] = A[i + 1]
        A[i + 1] = tmp
        i = 0
        print(f"Num is: {numm}. Massive is {A}")
    else: 
        numm += 1
        i += 1
        print(f"Num is: {numm}. Massive is {A}")


