package main

import (
	"context"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"log"
	"time"
)

type Wallet struct {
	// Объявляем структуру в bson формате для извлечения данных из MongoDB
	ID            primitive.ObjectID `bson:"_id,omitempty"`
	WallerAddress string             `bson:"waller_address"`
	WalletID      int                `bson:"wallet_id"`
	WalletInfo    *WalletInfo        `bson:"wallet_info"`
}

type WalletInfo struct {
	// Объявляем структуру в bson формате для извлечения вложенных данных из MongoDB
	Currency  string `bson:"currency"`
	Amount    int    `bson:"amount"`
	AmountUsd int    `bson:"amountUsd"`
}

func GetDataMongo() []Wallet {

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

	// Создаем курсор, которым будем итерироваться
	cursor, cursorErr := collection.Find(context.Background(), bson.D{})
	if cursorErr != nil {
		log.Fatal(cursorErr)
	}
	// Объявляем массив, куда будем складывать данные
	var wallet = []Wallet{}

	// Итерируемся по базе данных и складываем все в нащ массив
	for cursor.Next(context.Background()) {
		var result Wallet
		cursorErr := cursor.Decode(&result)
		if cursorErr != nil {
			log.Fatal(cursorErr)
		}
		wallet = append(wallet, result)
	}

	return wallet
}
