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

type wallet struct {
	WalletName    string //`bson:"walletName"`
	WalletAddress string //`bson:"walletAddress"`
}

func HashIndex() []string {
	timeStart := time.Now()

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

	cursor, cursorErr := collection.Find(context.Background(), bson.D{})
	if cursorErr != nil {
		log.Fatal(err)
	}

	var arr = []string{}

	for cursor.Next(context.Background()) {
		var res wallet
		cursorErr := cursor.Decode(&res)
		if cursorErr != nil {
			log.Fatal(cursorErr)
		}
		arr = append(arr, res.WalletAddress)
	}

	timeEnd := time.Now()
	fmt.Println(timeEnd.Sub(timeStart).Seconds())

	return arr
}

//func main() {
//	arr := HashIndex()
//	var x int
//	fmt.Scan(&x)
//	for x != 0 {
//		fmt.Println(arr[x])
//		fmt.Scan(&x)
//	}
//}
