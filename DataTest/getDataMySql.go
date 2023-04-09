package main

import (
	"database/sql"
	"fmt"
	"log"
)

func GetDataMySQL() []Person {
	db, err := sql.Open("mysql", "root:123123@/wallet_owner")
	if err != nil {
		log.Fatal(err)
	}

	defer db.Close()
	rows, err := db.Query("select * from wallet_owner.person")
	if err != nil {
		panic(err)
	}

	defer rows.Close()
	person := []Person{}

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
