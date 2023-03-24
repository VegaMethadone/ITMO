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
	WalletName    string `bson:"walletName"`
	WalletAddress string `bson:"walletAddress"`
}

func AddData(n int) {

	fake := faker.New()
	startTime := time.Now()

	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://localhost:27017"))
	if err != nil {
		log.Fatal(err)
	}
	ctx, _ := context.WithTimeout(context.Background(), 300*time.Second)
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}
	defer client.Disconnect(ctx)

	collection := client.Database("Laba").Collection("Wallets")

	// Создание индекса
	indexModel := mongo.IndexModel{
		Keys: bson.D{{"walletAddress", 1}},
	}
	name, err := collection.Indexes().CreateOne(context.TODO(), indexModel)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Name of Index Created: " + name)

	for i := 0; i < n; i++ {
		wallet := &Wallet{
			WalletName:    fake.Person().Name(),
			WalletAddress: fake.Crypto().EtheriumAddress(),
		}

		result, err := collection.InsertOne(context.Background(), wallet)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println(result.InsertedID)
	}

	endTime := time.Now()
	fmt.Println(endTime.Sub(startTime).Seconds())

}
