Зайти в файл hosts в системе
**Windows**
```shell
C:\Windows\System32\drivers\etc
```
Открываем hosts.txt и прописываем  порты для наших бд
```shell
Example: 127.0.0.1 <name>
127.0.0.1 mongo1
127.0.0.1 mongo2
127.0.0.1 mongo3
```
Создаем папку и создаем там файл docker-compose.yaml

Создание кластера MongoDB с 3-мя контейнерами  файле docker-compose.yaml
```yaml
version: '3.9'
services:
  mongo1:
    image: mongo
    container_name: mongo1
    #mem_limit: 0.1g
    storage_opt:
      size: 5G
    ports:
      - 27017:27017
    volumes:
      - ./data/db1:/data/db
    command: mongod --replSet "rs0" --port 27017 --bind_ip_all
    restart: "no"
    deploy:
      resources:
        limits:
          cpus: "1"
          memory: 100M
  mongo2:
    image: mongo
    container_name: mongo2
    #mem_limit: 0.1g
    storage_opt:
      size: 5G
    ports:
      - 27018:27018
    volumes:
      - ./data/db2:/data/db
    command: mongod --replSet "rs0" --port 27018 --bind_ip_all
    restart: "no"
    deploy:
      resources:
        limits:
          cpus: "1"
          memory: 100M
  mongo3:
    image: mongo
    container_name: mongo3
    #mem_limit: 0.1g
    storage_opt:
      size: 5G
    ports:
      - 27019:27019
    volumes:
      - ./data/db3:/data/db
    command: mongod --replSet "rs0" --port 27019 --bind_ip_all
    restart: "no"
    deploy:
      resources:
        limits:
          cpus: "1"
          memory: 100M 
```

Инициализация кластера
```shell
docker-compose up
```

Объявление репликации нод в самой бд. В нашем случае делаем mongo1 ведущей, остальыне  - ведомые  
```sql
rs.initiate({_id: "rs0", members: [
  {_id: 0, host: "mongo1:27017"},
  {_id: 1, host: "mongo2:27018"},
  {_id: 2, host: "mongo3:27019"}
]})
```

Проверяем, чтобы mongo1 была PRIMARY, остальные SECONDARY 
```sql
MongoDB Shell > mongosh
MongoDB Shell > rs.status()
```
Запуск скрипта для убийства бд
```shell
python3 main.py
```
