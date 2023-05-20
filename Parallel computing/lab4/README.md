Компиляция Сфайла для тестов 

```shell
clang -O3 -Wall -Werror -fopenmp lab4.c -o lab-4 -lm -lgomp
```

Компиляция полученных файлов
```shell
python3 build.py
```

```shell
OMP_NUM_THREADS={cores} OMP_DYNAMIC=FALSE
```


```shell
OMP_NUM_THREADS=4 OMP_DYNAMIC=FALSE clang -O3 -Wall -Werror -fopenmp lab4.c -o lab-4 -lm -lgomp
```

```shell
clang -O3 -Wall -Werror -fopenmp test.c -o test -lm -lgomp
```