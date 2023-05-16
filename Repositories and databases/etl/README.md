> Создание базы данных для MySQl
> > Зайти через терминал docker в mysql
>> ```shell
>> mysql -u root -p
>> 123123
>> ```
> >Создать базу данных и таблицы
>>```shell
>>create database wallet_owner;
>>use wallet_owner;
>>create table person (
>>    id int auto_increment primary key,
>>    wallet_id int not null,
>>    first_name text not null,
>>    last_name text not null,
>>    country text not null,
>>    city text not null,
>>    district text not null
>>)
>>```

> Создание базы данных PostgresSQL
>>
>>Заходим в терминал
>>```shell
>>su postgres
>> 123123
>>psql
>>````
>>Создаем базу данных
>>```shell
>>create database bank;
>>```
>>Заходи в базу данных
>>```shell
>>\c bank;
>>use bank - если через pgAdmin
>>```
>>
>>Создаем базу данных Person
>>```shell
>>create table Person (
>>    id serial primary key,
>>    first_name text not null,
>>    last_name text not null,
>>    country text not null,
>>    city text not null,
>>    district text not null
>>)
>>```
>>
>>Создаем базу данных Wallet 
>>```shell
>>create table Wallet (
>>    id serial primary key,
>>    wallet_address text not null,
>>    wallet_id int not null,
>>    currency text not null,
>>    amount int not null,
>>    amount_usd int not null
>>)
>>```



