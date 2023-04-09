```

** Создание базы данных для MySQl **

create database wallet_owner;
use wallet_owner;
create table person (
id int auto_increment primary key,
wallet_id int not null,
first_name text not null,
last_name text not null,
country text not null,
city text not null,
district text not null
)

** Создание базы данных PostgresSQL **

create database bank

use bank

create table Person (
    id serial primary key,
    first_name text not null,
    last_name text not null,
    country text not null,
    city text not null,
    district text not null
)

create table Wallet (
    id serial primary key,
    wallet_address text not null,
    wallet_id int not null,
    currency text not null,
    amount int not null,
    amount_usd int not null
)