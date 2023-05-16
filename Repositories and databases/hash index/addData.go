package main

import (
	"context"
	"fmt"
	"github.com/jaswdr/faker"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"log"
	"time"
)

type Wallet struct {
	//Объявляем структуру хранения данных в формате bson (Формат под MongoDB)
	WalletName    string `bson:"walletName"`
	WalletAddress string `bson:"walletAddress"`
}

func AddData(n int) {
	fake := faker.New()
	startTime := time.Now()

	// Подключение к базе данных
	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://localhost:27017"))
	// Вывод ошибки в случае err будет содержать в себе значение, отличное от nil
	if err != nil {
		log.Fatal(err)
	}

	//Задаем контекст подключниея, в случае которого мы отключяимся от БД (TimeLimit 300 sec)
	ctx, _ := context.WithTimeout(context.Background(), 300*time.Second)
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}

	// В конце программы обязательно закрыть подключние к БД
	defer client.Disconnect(ctx)

	collection := client.Database("Laba").Collection("Wallets")

	// Создание индекса в нашем файле
	indexModel := mongo.IndexModel{
		Keys: bson.D{{"walletAddress", 1}},
	}

	// Индексируем наш файл
	name, err := collection.Indexes().CreateOne(context.TODO(), indexModel)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Name of Index Created: " + name)

	// Добавление самих данных в нашу БД
	for i := 0; i < n; i++ {
		//Создаем документ с типом данных, который мы указывали в начале
		wallet := &Wallet{
			WalletName:    fake.Person().Name(),
			WalletAddress: fake.Crypto().EtheriumAddress(),
		}

		// Добавление документа в БД
		result, err := collection.InsertOne(context.Background(), wallet)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println(result.InsertedID)
	}

	// Выводим время добавления документов
	endTime := time.Now()
	fmt.Println(endTime.Sub(startTime).Seconds())

}
