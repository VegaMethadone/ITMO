#Установка Docker-Engine Linux
```shell
sudo apt-get remove docker docker-engine docker.io containerd runc
```
Обновление индекс пакета apt и установка пакетов, чтобы разрешить apt использовать репозиторий по протоколу HTTPS:
```shell
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg
```
Добавление официального GPG-ключа Docker:

```shell
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
Настрока репозитория:
```shell
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
Обновление apt пакета:
```shell
sudo apt-get update
```
Установка Docker Engine, контейнер и Docker Compose:
```shell
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
Верификация Docker-Engine: 
```shell
sudo docker run hello-world
```

Установка Docker linux: 
```shell
sudo apt-get update
sudo apt-get install ./docker-desktop-<version>-<arch>.deb
```

Запуск Docker DeskTop:
```shell
systemctl --user start docker-desktop
```

Установка Postgres Docker Image:
```shell
docker pull postgres
```
Установка MySQL Docker Image:
```shell
docker pull mysql
```
Установка MongoDB Docker Image:
```shell
docker pull mongo
```


Создание базы данных для MySQl 

```sql
CREATE DATABASE wallet_owner;
USE wallet_owner;
CREATE TABLE person (
id int auto_increment primary key,
wallet_id int not null,
first_name text not null,
last_name text not null,
country text not null,
city text not null,
district text not null
);
```

Создание базы данных PostgresSQL

```sql
CREATE DATABASE bank;

USE bank;
CREATE TABLE Person (
    id serial primary key,
    first_name text not null,
    last_name text not null,
    country text not null,
    city text not null,
    district text not null
);

CREATE TABLE Wallet (
    id serial primary key,
    wallet_address text not null,
    wallet_id int not null,
    currency text not null,
    amount int not null,
    amount_usd int not null
);
```
