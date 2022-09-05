# for i in range(200,500):
#     x = i
#     L = 2 * x - 20
#     M = 2 * x + 30
#     while L != M:
#         if L > M:
#             L = L - M
#         else:
#             M = M - L
#     if M == 50:
#         print(f" INDEX: {i}")


x = int(input())
L = 2 * x - 20
M = 2 * x + 30
while L != M:
    if L > M:
        L = L - M
    else:
        M = M - L
print(M)
