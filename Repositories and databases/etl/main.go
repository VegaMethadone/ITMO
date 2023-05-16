package main

import "fmt"

func main() {
	var n int
	fmt.Println("Введите число")
	fmt.Scan(&n)
	fmt.Println("Генерация данных MySql")
	InsertDataMySQl(n)
	fmt.Println("Генерация данных Mongo")
	InsertDataMongo(n)
	fmt.Println("Получение данных MySql")
	person := GetDataMySQL()
	fmt.Println("Получение данных Mongo")
	wallet := GetDataMongo()
	fmt.Println("Реализация ETL")
	person, wallet = ETL(person, wallet)
	fmt.Println("Добавление данных Postgres")
	PostDataPostgres(person, wallet)
}
