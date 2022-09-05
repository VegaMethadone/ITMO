function_text = input("Введите функцию от Х:")
f = lambda x: eval(function_text)
a, b = [float(word) for word in input("Промежуток для поиска корней (два числа через пробел").split()]
x = (a + b) / 2
error = float(input("С какой погрешностью ищем корень: "))
if f(a) * f(b) >= 0:
    print("нельзя воспользоваться двоичным поиском точек")
    exit(0)
while  (b - a) / 2 > error:
    c = (a + b) / 2
    if f(c) == 0:
        break #  koren'
    elif f(a) * f(c) < 0:
        b = c
    else: # f(a) * f(c) > 0
        a = c
print(f"Корень f(x) = 0: {(a + b) / 2} +-  {(b - a) / 2}")
