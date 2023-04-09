package main

import (
	"encoding/json"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	_ "github.com/lib/pq"
	"log"
	"os"
	"strings"
)

type Person struct {
	ID        int
	WalletId  int
	FirstName string
	LastName  string
	Country   string
	City      string
	District  string
}

func checker(str string, symbols []string) string {
	for i := 0; i < len(symbols); i++ {
		str = strings.ReplaceAll(str, symbols[i], "")
	}

	return str
}

func Transform(person Person, wallet Wallet) (Person, Wallet) {

	p := person
	p.FirstName = checker(p.FirstName, Symbols)
	p.LastName = checker(p.LastName, Symbols)
	p.Country = checker(p.Country, Symbols)
	p.City = checker(p.City, Symbols)
	p.District = checker(p.District, Symbols)

	w := wallet
	w.WallerAddress = checker(w.WallerAddress, Symbols)
	w.WalletInfo.Currency = checker(w.WalletInfo.Currency, Symbols)

	return person, wallet
}

func ETL(person []Person, wallet []Wallet) ([]Person, []Wallet) {

	var data []MetaData

	for i := 0; i < len(wallet); i++ {

		tmpPerson, tmpWallet := Transform(person[i], wallet[i])

		postgresDataWallet := PostgresDataWallet{
			WalletAddress: tmpWallet.WallerAddress,
			WalletId:      tmpWallet.WalletID,
			Currency:      tmpWallet.WalletInfo.Currency,
			Amount:        tmpWallet.WalletInfo.Amount,
			AmountUsd:     tmpWallet.WalletInfo.AmountUsd,
		}

		postgresDataPerson := PostgresDataPerson{
			WalletId:  tmpPerson.WalletId,
			FirstName: tmpPerson.FirstName,
			LastName:  tmpPerson.LastName,
			Country:   tmpPerson.Country,
			City:      tmpPerson.City,
			District:  tmpPerson.District,
		}

		postgresDataInfo := PostgresDataInfo{
			PostgresDataPerson: []PostgresDataPerson{postgresDataPerson},
			PostgresDataWallet: []PostgresDataWallet{postgresDataWallet},
		}

		mongoDataWalletInfo := MongoDataWalletInfo{
			Currency:  wallet[i].WalletInfo.Currency,
			Amount:    wallet[i].WalletInfo.Amount,
			AmountUsd: wallet[i].WalletInfo.AmountUsd,
		}

		mongoDataWallet := MongoDataWallet{
			WalletAddress:       wallet[i].WallerAddress,
			WalletId:            wallet[i].WalletID,
			MongoDataWalletInfo: []MongoDataWalletInfo{mongoDataWalletInfo},
		}

		mySqlDataPerson := MySqlDataPerson{
			MySqlId:   person[i].ID,
			WalletId:  person[i].WalletId,
			FirstName: person[i].FirstName,
			LastName:  person[i].LastName,
			Country:   person[i].Country,
			City:      person[i].City,
			District:  person[i].District,
		}

		newData := MetaData{
			MySqlId:          person[i].ID,
			MongoId:          wallet[i].ID,
			PostgresId:       person[i].ID,
			MySqlDataPerson:  []MySqlDataPerson{mySqlDataPerson},
			MongoDataWallet:  []MongoDataWallet{mongoDataWallet},
			PostgresDataInfo: []PostgresDataInfo{postgresDataInfo},
		}

		data = append(data, newData)

		person[i], wallet[i] = tmpPerson, tmpWallet
	}

	jsonData, err := json.MarshalIndent(data, "", "\t")
	if err != nil {
		log.Fatal(err)
	}

	err = os.WriteFile("meta.json", jsonData, 0644)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Print("JSON записан в Файле data.json")

	return person, wallet
}
