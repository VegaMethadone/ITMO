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

func AddByHand() string {
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

	var newWalletName string
	var newWalletAddress string
	fmt.Println("Wallet Name:\t")
	fmt.Scan(&newWalletName)
	fmt.Println("Wallet Address:\t")
	fmt.Scan(&newWalletAddress)

	insert := bson.D{
		{"walletName", newWalletName},
		{"walletAddress", newWalletAddress},
	}

	result, err := collection.InsertOne(context.Background(), insert)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Added data with ", result.InsertedID)

	/*if len(freeCeels) != 0 {
		var allocateIndex int
		allocateIndex = freeCeels[0]
		arr[allocateIndex] = newWalletAddress
		fmt.Println("Index of new data is: ", freeCeels[0])
		freeCeels = freeCeels[0:]
	} else {
		arr = append(arr, newWalletAddress)
	}
	*/
	return newWalletAddress

}
