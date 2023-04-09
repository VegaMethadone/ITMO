package main

import "fmt"

func main() {
	var n int
	fmt.Scan(&n)
	InsertDataMySQl(n)
	InsertDataMongo(n)
	person := GetDataMySQL()
	wallet := GetDataMongo()
	person, wallet = ETL(person, wallet)
	PostDataPostgres(person, wallet)
}
