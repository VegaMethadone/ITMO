package main

import (
	"context"
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"github.com/jaswdr/faker"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"log"
	"math/rand"
	"time"
)

// Создаем данные, которые будут содержать невалидные символы для дальнейшей трансформации данных
var global int = 1
var Symbols = []string{"!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "№", ";", ":", "?", "/", "[", "]", "{", "}"}

func RandNumber(arr []string) int {
	// рандомно выбираем один из доступных символов выше
	randomizer := rand.Intn(len(arr) - 0)
	return randomizer
}

func InsertDataMySQl(n int) {

	// Подключаемся к базе данных через доступные драйвер
	db, err := sql.Open("mysql", "root:123123@/wallet_owner")
	// Если err веренул значение отличное от nil, нам выводится наша ошибка
	if err != nil {
		log.Fatal(err)
	}

	// Закрываем подключение к БД
	defer db.Close()

	fake := faker.New()
	for i := 1; i <= n; i++ {

		// В конце к нашим данным добавляется рандомный символ
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

		// Сам запрос на добавление базы данных в MySQL
		insert := fmt.Sprintf("insert into wallet_owner.person (wallet_id, first_name, last_name, country, city, district) values ('%d', '%s', '%s', '%s', '%s', '%s')", walletId, firstNameV2, lastNameV2, countryV2, cityV2, districtV2)

		// Исполнение нашего запроса
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

	// Подключение к базе данных MongoDB через драйвер
	mongoClient, err := mongo.NewClient(options.Client().ApplyURI("mongodb://localhost:27017"))
	// Если err веренул значение отличное от nil, нам выводится наша ошибка
	if err != nil {
		log.Fatal(err)
	}

	// Задем контекст при котором мы  будем отключены от базы данных
	ctx, _ := context.WithTimeout(context.Background(), 300*time.Second)
	err = mongoClient.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}

	// Закрываем подключение к БД
	defer mongoClient.Disconnect(ctx)

	collection := mongoClient.Database("Wallets").Collection("Wallet")

	//Добавление наших данных в БД
	for i := 1; i <= n; i++ {
		tmpInt := fake.IntBetween(1, 1000)
		walletInfo := &WalletInfo{
			Currency:  "Eth" + Symbols[RandNumber(Symbols)],
			Amount:    tmpInt,
			AmountUsd: tmpInt * 1909,
		}
		wallet := &Wallet{
			ID:            primitive.NewObjectID(),
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
