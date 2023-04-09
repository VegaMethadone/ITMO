package main

import (
	"context"
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"github.com/jaswdr/faker"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"log"
	"math/rand"
	"time"
)

var global int = 1
var Symbols = []string{"!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "№", ";", ":", "?", "/", "[", "]", "{", "}"}

func RandNumber(arr []string) int {
	randomizer := rand.Intn(len(arr)-0) + 0
	return randomizer
}

func InsertDataMySQl(n int) {

	db, err := sql.Open("mysql", "root:123123@/wallet_owner")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	fake := faker.New()
	for i := 1; i <= n; i++ {

		var walletId int = i
		firstName := fake.Person().Name()
		firstNameV2 := firstName + Symbols[RandNumber(Symbols)]
		lastName := fake.Person().LastName()
		lastNameV2 := lastName + Symbols[RandNumber(Symbols)]
		country := fake.Address().Country()
		countryV2 := country + Symbols[RandNumber(Symbols)]
		city := fake.Address().City()
		cityV2 := city + Symbols[RandNumber(Symbols)]
		district := fake.Address().StreetName()
		districtV2 := district + Symbols[RandNumber(Symbols)]

		insert := fmt.Sprintf("insert into wallet_owner.person (wallet_id, first_name, last_name, country, city, district) values ('%d', '%s', '%s', '%s', '%s', '%s')", walletId, firstNameV2, lastNameV2, countryV2, cityV2, districtV2)

		result, err := db.Exec(insert)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println(result.LastInsertId())
		global += 1
	}
}

func InsertDataMongo(n int) {

	fake := faker.New()
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

	for i := 1; i <= n; i++ {
		tmpInt := fake.IntBetween(1, 1000)
		walletInfo := &WalletInfo{
			Currency:  "Eth" + Symbols[RandNumber(Symbols)],
			Amount:    tmpInt,
			AmountUsd: tmpInt * 1909,
		}
		wallet := &Wallet{
			WallerAddress: fake.Crypto().EtheriumAddress(),
			WalletID:      i,
			WalletInfo:    walletInfo,
		}

		result, err := collection.InsertOne(context.Background(), wallet)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println(result.InsertedID)
	}
}
