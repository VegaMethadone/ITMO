function_text = input("Function: ")
a, b = [float(word) for word in input("Distance 1)A 2)B ").split()]

x = (a + b) / 2
f = lambda x: eval(function_text)
error = float(input("Error: "))
if f(a) * f(b) >= 0:
    print("Нельзя воспользоваться двоичным поиском")
    exit(0)
while (b - a) / 2 > error:
    c = (a + b) / 2
    if f(c) == 0:
        print(f"Корень: {f(c)} погрешность: {error}")
    elif f(c) * f(a) < 0:
        a = a
        c = b
    elif f(c) * f(b) < 0:
        b = b
        a = c    
print(f"Корень f(x) = 0: {(a + b) / 2} с погрешностью +- : {(b - a) / 2}")