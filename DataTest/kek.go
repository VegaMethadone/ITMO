package main

import (
	"encoding/json"
	"fmt"
	"github.com/jaswdr/faker"
	"log"
	"os"
)

type TransactionInfo struct {
	MongoID       int            `json:"mongo_id"`
	MySqlID       int            `json:"my_sql_id"`
	PostgresSqlID int            `json:"postgres_sql_id"`
	MongoData     []MongoData    `json:"mongo_data"`
	MySqlData     []MySqlData    `json:"my_sql_data"`
	PostgresData  []PostgresData `json:"postgres_data"`
}

type MongoData struct {
	MongoID       int           `json:"mongo_id"`
	WalletName    string        `json:"wallet_name"`
	WalletAddress string        `json:"wallet_address"`
	MongoWallet   []MongoWallet `json:"mongo_wallet"`
}

type MongoWallet struct {
	Currency    string `json:"currency"`
	Amount      int    `json:"amount"`
	AmountInUsd int    `json:"amount_in_usd"`
}

type MySqlData struct {
	MySqlId         int        `json:"my_sql_id"`
	WalletOwner     string     `json:"wallet_owner"`
	WalletOwnerName string     `json:"wallet_owner_name"`
	Address         *Address   `json:"address"`
	Contacts        []Contacts `json:"contacts"`
}

type Address struct {
	Country       string `json:"country"`
	City          string `json:"city"`
	Neighbourhood string `json:"neighbourhood"`
}

type Contacts struct {
	Phone string `json:"phone"`
	Email string `json:"email"`
}

type PostgresData struct {
	PostgresSqlID int    `json:"postgres_sql_id"`
	WalletAddress string `json:"wallet_address"`
	Currency      string `json:"currency"`
	Amount        int    `json:"amount"`
	AmountInUsd   int    `json:"amount_in_usd"`
}

func jsonCreation2(n int) {
	var data []TransactionInfo
	for i := 0; i < n; i++ {

		tmp_cur := faker.New().IntBetween(1, 1000)
		tmp_owner := faker.New().Crypto().EtheriumAddress()
		mongoWallet := MongoWallet{
			Currency:    "Etherium",
			Amount:      tmp_cur,
			AmountInUsd: tmp_cur * 1909,
		}

		mongoData := MongoData{
			MongoID:       i,
			WalletName:    faker.New().Pet().Name(),
			WalletAddress: tmp_owner,
			MongoWallet:   []MongoWallet{mongoWallet},
		}

		address := &Address{
			Country:       faker.New().Address().Country(),
			City:          faker.New().Address().City(),
			Neighbourhood: faker.New().Address().StreetName(),
		}

		contacts := Contacts{
			Phone: faker.New().Phone().Number(),
			Email: "Ifanov@gmail.com",
		}

		mySqlData := MySqlData{
			MySqlId:         i,
			WalletOwner:     tmp_owner,
			WalletOwnerName: faker.New().Person().Name(),
			Address:         address,
			Contacts:        []Contacts{contacts},
		}

		postgresData := PostgresData{
			PostgresSqlID: i,
			WalletAddress: tmp_owner,
			Currency:      "Etherium",
			Amount:        tmp_cur,
			AmountInUsd:   tmp_cur * 1909,
		}
		newData := TransactionInfo{
			MongoID:       i,
			MySqlID:       i,
			PostgresSqlID: i,
			MongoData:     []MongoData{mongoData},
			MySqlData:     []MySqlData{mySqlData},
			PostgresData:  []PostgresData{postgresData},
		}
		data = append(data, newData)
	}

	jsonData, err := json.MarshalIndent(data, "", "    ")
	if err != nil {
		log.Fatal(err)
	}

	err = os.WriteFile("wallets.json", jsonData, 0644)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Print("JSON записан в Файле data.json")
}
