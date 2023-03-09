package main

import (
	"context"
	"fmt"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"log"
	"time"
)

func ReadDB() {
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

	cursor, err := startCollection.Find(ctx, bson.M{})
	if err != nil {
		log.Fatal(err)
	}

	defer cursor.Close(ctx)
	for cursor.Next(ctx) {
		var tmpData bson.M
		if err = cursor.Decode(&tmpData); err != nil {
			log.Fatal(err)
		}
		fmt.Println(tmpData)
	}
	endTime := time.Now()
	fmt.Println(endTime.Sub(startTime).Seconds())
}
