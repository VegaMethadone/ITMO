A = [int(x) for x in input().split()]
B = [int(x) for x in input().split()]

def combine_massibve(A, B):
    """ Возвращение обхеденного массива + сортировка"""
    i = 0
    k = 0
    n = 0
    C = [None]* (len(A) + len(B))
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
        k += 1
        n += 1
    
    return C

print(combine_massibve(A, B))
