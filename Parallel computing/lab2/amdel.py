import matplotlib.pyplot as plt 

# P = 16

K = 14 / (14 + 3) # Так как у меня 14 функций из библиотеки и 3 цикла  - Доля распараллеленых программ = 0.824
K2 = 0.824
print(K)
print(K2)

#Amdel  - 1 / (k/p + 1 - k), где p - число процессоров

y = []
x = []

for p in range(1, 9):
    print(p)
    y.append(p)
    tmp = 1 / (K2/p + 1 - K2)
    x.append(tmp)


plt.plot(y, x, label='amdel')
plt.xlabel("p")
plt.ylabel("Exec ms")
plt.legend(loc="upper left")
plt.savefig('amdal.png')
plt.clf()
