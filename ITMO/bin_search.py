import random
import re
from turtle import right

A = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def search(A, key):
    left = -1
    right = max(A)
    while right > left + 1:
        middle = (left + right) // 2
        if A[middle] > key:
            right = middle
        else:
            left = middle
    if left >= 0 and A[left] == key:
        return left

print(search(A, 7))
