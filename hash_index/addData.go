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

func FillDatabase(n int) {
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
	startDatabase := client.Database("lab")
	startCollection := startDatabase.Collection("laba")

	for i := 0; i < n; i++ {
		result, err := startCollection.InsertOne(ctx, bson.D{
			{"currency", "Etherium"},
			{"from", fake.Crypto().EtheriumAddress()},
			{"to", fake.Crypto().EtheriumAddress()},
			{"transactionIndex", i},
		})
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println(result.InsertedID)
	}

	endTime := time.Now()
	fmt.Println(endTime.Sub(startTime).Seconds())
}
