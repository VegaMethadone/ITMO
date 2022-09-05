A = list(range(1, 25+1))
B = [0] * len(A)
for i in range(len(A)):
    B[i] = A[len(A) - 1 - i]
print(A)
print(B)