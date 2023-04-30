1. Создание файла
```shell
python3 build.py
```

2. Считаем время 
```shell
python3 acceleration_time.py
```

3. Сравниваем графики 3 лабораторных
```shell
python3 acceleartion_common.py
```

4. Строим график параллельного ускорения всех работ
```shell
python3 acceleration_json_maker.py
```

5. Установка расписания
```cpp
omp_set_schedule(omp_sched_x, N);  x --> [dynamic, static, guided]
        #pragma omp parallel for default(none) shared(M2, arr2, arr2Coppy, A, seed) schedule(dynamic, N) firstprivate(N)
```
