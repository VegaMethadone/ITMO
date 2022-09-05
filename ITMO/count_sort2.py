

A = [0, 4, 1, 3, 5, 7, 9, 0, 1, 5, 2, 5, 7, 8, 3, 5, 6, 9, 9, 2, 3]

N= len(A)
F = [0] * 10
for x in A:
    F[x] += 1
i = 0
for x in range(0, 10):
    for k in range(F[x]):
        A[i] = x
        i += 1
        print(i)