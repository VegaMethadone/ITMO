
A = [1, 22, 53, 85, 74, 6, 8, 37, 47, 54, 41, 62, 71, 85, 94, 16, 12, 21, 12, 13, 15, 14, 12, 10, 15, 13,
     19, 17, 18, 21, 94, 5, 2, 24, 21, 22, 22, 74, 65, 24, 21, 23, 8, 25, 26, 27, 28, 21, 35, 34, 21, 74, 87]

N = len(A)
numm = 0
for bypass in range(N - 1):
    for i in range(N - 1):
        if A[i] > A[i + 1]:
            tmp = A[i]
            A[i] = A[i + 1]
            A[i + 1] = tmp
            numm += 1
            #print(f"Number: {numm}. Massive: {A}")
        print(A[N//2])



































































#A = [1, 22, 53, 85, 74, 6, 8, 37, 47, 54, 41, 62, 71, 85, 94, 16, 12, 21, 12, 13, 15, 14, 12, 10, 15, 13,
#    19, 17, 18, 21, 94, 5, 2, 24, 21, 22, 22, 74, 65, 24, 21, 23, 8, 25, 26, 27, 28, 21, 35, 34, 21, 74, 87]
#N = len(A)
#numm = 0
#for bypass in range(N - 1):
#    for i in range(N - 1):
#        if A[i] > A[i + 1]:
#            tmp = A[i]
#            A[i] = A[i + 1]
#            A[i + 1] = tmp
#            numm += 1
#            print(f"Number: {numm}. Massive: {A}")
