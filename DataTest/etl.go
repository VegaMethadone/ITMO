package main

import (
	"context"
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"log"
	"strings"
	"time"
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

type walletEarn struct {
	WallerAddress  string          `bson:"waller_address"`
	WalletID       int             `bson:"wallet_id"`
	WalletInfoEarn *walletInfoEarn `bson:"wallet_info"`
}

type walletInfoEarn struct {
	Currency  string `bson:"currency"`
	Amount    int    `bson:"amount"`
	AmountUsd int    `bson:"amountUsd"`
}

func checker(str string, symbols []string) string {
	for i := 0; i < len(symbols); i++ {
		str = strings.ReplaceAll(str, symbols[i], "")
	}
	return str
}

func TakeDataMySQL() []Person {
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
	/*for _, p := range person {
		fmt.Println(p.ID, p.WalletId, p.FirstName, p.LastName, p.Country, p.City, p.District)
	}

	*/

	return person
}

func TakeDataMongo() []walletEarn {
	mongoClient, err := mongo.NewClient(options.Client().ApplyURI("mongodb://localhost:27017"))
	if err != nil {
		log.Fatal(err)
	}
	ctx, _ := context.WithTimeout(context.Background(), 300*time.Second)
	err = mongoClient.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}
	defer mongoClient.Disconnect(ctx)

	collection := mongoClient.Database("Wallets").Collection("Wallet")

	cursor, cursorErr := collection.Find(context.Background(), bson.D{})
	if cursorErr != nil {
		log.Fatal(cursorErr)
	}
	var wallet = []walletEarn{}

	for cursor.Next(context.Background()) {
		var result walletEarn
		cursorErr := cursor.Decode(&result)
		if cursorErr != nil {
			log.Fatal(cursorErr)
		}
		wallet = append(wallet, result)
	}

	return wallet
}

func etl(person []Person, wallet []Wallet) ([]Person, []Wallet) {
	for _, p := range person {
		p.FirstName = checker(p.FirstName, symbols)
		p.LastName = checker(p.LastName, symbols)
		p.Country = checker(p.Country, symbols)
		p.City = checker(p.City, symbols)
		p.District = checker(p.District, symbols)
	}
	for _, w := range wallet {
		w.WallerAddress = checker(w.WallerAddress, symbols)
		w.WalletInfo.Currency = checker(w.WalletInfo.Currency, symbols)
	}
	return person, wallet
}
