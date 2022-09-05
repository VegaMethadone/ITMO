A = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def shift_left():
    "Циклический сдвиг влево (поэлементно)"
    tmp  = A[0]
    for i in range(0, len(A)-1):
        A[i] = A[i+1] # В текущий кладку значение следующего
        print(f"Debug: {i}, {A}")
    A[len(A)-1] = tmp

def shift_right():
    "Циклический свдиг вправо (поэлементно)"
    tmp = A[len(A)-1]
    for i in range(len(A)-2 , -1 , -1):
        A[i+1] = A[i] # В следующий - значение текущего
        print(f"Debug: {i}, {A}")
    A[0] = tmp
