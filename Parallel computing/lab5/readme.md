Компиляция с файла
```shell
clang -O3 -Wall -Werror -pthread lab5.c -o lab-5 -lm -lgomp
```


Тестовая сборка
```shell
clang -O3 -Wall -Werror -fopenmp -pthread test.c -o test -lm -lgomp
```

При передаче аргументов через консоль второй аргумент не может быть меньше двух т.к. 1 поток всегда забирает progressBar
```shell
1 < NTHREADS < 9
```