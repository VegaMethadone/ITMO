import random
A = [0] * 200
for kek in range(200):
    A[kek] = random.randint(1, 200)
print(*A)


is_sorted = False
N = len(A)
numm = 0
while not is_sorted:
    is_sorted = True
    i = 0
    while i < N - 1:
        if A[i] > A[i + 1]:
            tmp = A[i] # Save my index
            A[i] = A[i + 1] #Replace index
            A[i + 1] = tmp  # Replace index
            is_sorted = False 
            numm += 1 # Check how many operations were done
        i += 1
        print(f"Number is: {numm}. Massive is: {A}")