```shell
Заменить в parallel_time.json target-clang на CLANG
Переместить divide.json  в ппапку assets
Переместить time_data.json в assets
```


Сборка эксперементов
```shell
python3 build.py
```

Запуск эксперементов
```shell
python3 acceleration_time.py
```

Создание первичного графика, который сравнивает время выполнения 3-ёх лабараторных
```shell
python3 acceleration_common.py
```

Создание графика параллельного ускорения 
```shell
python3 acceleration_json_maker.py
```

Сборка билдов с установленным расписанием
```shell
python3 build_schedule_dynamic.py
python3 build_schedule_guided.py
python3 build_schedule_static.py
```

Сборка билда и выявление типа расспиание, которое машина использует по умолчанию
```shell
python3 build_schedule_auto.py
```
Запуск С файлов с различными типами расписания
```shell
python3 run_schedule.py
```

Сборка оптимизированных либдов с другими флагами оптимизации
```shell
python3 optimisation_build.py
```

Запуск билдов оптимизации
```shell
python3 optimisation_build.py
```

Запуск для определенных N  для поиска параллельного ускорения и накладных расходов
```shell
python3 parallel_acceleration.py
```