for i in range(1000):
    x = i
    L = 0
    M = 0
    while x > 0:
      L += 1
      if x % 2 == 0:
        M += x % 10
      x //= 10
    if L == 3 and M == 0:
        print(f"Number L is: {L}")
        print(f"Number M is: {M}")
        print(f"Number is: {i}")