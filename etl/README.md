#Создание базы данных для MySQl 


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

#Создание базы данных PostgresSQL

```sql
CREATE DATABASE bank

USE bank
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
