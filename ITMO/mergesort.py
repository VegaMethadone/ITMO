def merge(A,B):
    '''возвращает C'''
    C = [None]*(len(A)+len(B))
    i = 0
    k = 0
    n = 0
    while i < len(A) and k < len(B):
        if A[i] <= B[k]:
            C[n] = A[i]
            i += 1
            n += 1
        else:
            C[n] = B[k]
            k += 1
            n += 1

    while i < len(A):
        C[n] = A[i]
        i += 1
        n += 1

    while k < len(B):
        C[n] = B[k]
        k += 1
        n += 1 
              
    return C


A = [int(x) for x in input().split()]
B = [int(x) for x in input().split()]
print(merge(A,B))