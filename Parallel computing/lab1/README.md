Обновляем менеджер пакетов
```shell
sudo apt-get update
```
Установка компиляторов gcc, gcc, clang
```shell
sudo apt-get install gcc
sudo apt-get install gcc
sudo apt-get install clean
```
Компилируем получившуюся программу на С
```shell
python3 build.py
```
Вычисляем N1 && N2 массива для NO_PARALLEL программ, такой, что N1 = 1000, N2 = 5000
```shell
python3 noparallel.py
```
Находим N△, такой, что (N2 - N1) / 10 ---> ((N1 + N△) + N△) + N△ ..... + N△ = N2
```shell
python3 paralleling.py
```
Запускаем программу для всех компиляторов c разными параметрами использования ядер для всех Ni, ~~где Ni = N[((N1 + N°) + N°) + N° ..... + N°]~~, 
чтобы вычислить время испольнения программы
```shell
python3 timing.py
```
Строим по полученным данным графики производительности автоматического распараллеливания
```shell
python3 graph.py
```
