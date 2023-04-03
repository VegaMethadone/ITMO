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

func Delete(arr []string, freeCells []int, index int) ([]string, []int) {
	// Подключение к базе данных
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

	result, err := collection.DeleteOne(context.Background(),
		bson.D{{"walletAddress", arr[index]}})
	if err != nil {
		log.Fatal(err)
	}

	arr[index] = "nil"
	freeCells = append(freeCells, index)

	fmt.Printf("Удаленно %v Документов!\n", result.DeletedCount)

	return arr, freeCells
}
