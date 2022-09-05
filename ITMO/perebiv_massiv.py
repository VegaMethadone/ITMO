from sys import float_repr_style


function_text = input("Введиет функцию от Х: ")
a, b = [int(word) for word in input("Поиск корня ( два числа через пробел): ").split()]
f = lambda x: eval(function_text)
error = float(input("С какой погрешностью ищем коернь"))
if f(a) * f(b) > 0:
    print("Не вохможно вычислить корень")
    exit(0)
while (a + b) / 2 > error:
    c = (a + b) / 2
    if f(c) == 0:
        print(f(c))
        break
    elif f(a) * f(c) < 0:
         b = c
