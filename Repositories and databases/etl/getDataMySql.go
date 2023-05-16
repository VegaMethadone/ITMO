package main

import (
	"database/sql"
	"fmt"
	"log"
)

func GetDataMySQL() []Person {

	// Подключаемся к базе данных через доступные драйвер
	db, err := sql.Open("mysql", "root:123123@/wallet_owner")
	if err != nil {
		log.Fatal(err)
	}

	defer db.Close()
	rows, err := db.Query("select * from wallet_owner.person")
	// Если err веренул значение отличное от nil, нам выводится наша ошибка
	if err != nil {
		log.Fatal(err)
	}

	// Закрываем подключение к БД
	defer rows.Close()

	// Инициализируем массив, куда будем складывать наши данные типа Person
	// p.s. само объявление Person находится в файлу etl.go
	person := []Person{}

	// Извлечение данных из MySQL
	for rows.Next() {
		p := Person{}
		err := rows.Scan(&p.ID, &p.WalletId, &p.FirstName, &p.LastName, &p.Country, &p.City, &p.District)
		if err != nil {
			fmt.Println(err)
			continue
		}
		person = append(person, p)
	}

	return person
}
