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

func Update(value string) string {
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
	//filter := bson.D{{"walletAddress", value}}

	// Тоже самое, что и добавление, только updateOne
	var value2 string
	fmt.Print("Что заменить?\n 1)WalletName\n 2)WalletAddress\n 3)Все\n 0)Выход\n")
	var option int
	fmt.Scan(&option)
	for option != 0 {
		if option == 1 {
			var walletName string
			fmt.Println("WalletName:\t")
			fmt.Scan(&walletName)

			startTime := time.Now()

			//update := bson.D{{"$set", bson.D{{"walletName", walletName}}}}

			result, err := collection.UpdateOne(
				context.Background(),
				bson.D{{"walletAddress", value}},
				bson.D{{"$set", bson.D{{"walletName", walletName}}}})
			if err != nil {
				log.Fatal(err)
			}

			endTime := time.Now()
			fmt.Printf("Обновленно %v Документов!\n", result.ModifiedCount)
			fmt.Println(endTime.Sub(startTime).Seconds())

			value2 = value
			return value2

		} else if option == 2 {
			var walletAddress string
			fmt.Println("WalletAddress:\t")
			fmt.Scan(&walletAddress)

			startTime := time.Now()

			result, err := collection.UpdateOne(
				context.Background(),
				bson.D{{"walletAddress", value}},
				bson.D{{"$set", bson.D{{"walletAddress", walletAddress}}}})
			if err != nil {
				log.Fatal(err)
			}

			endTime := time.Now()

			fmt.Printf("Обновленно %v Документов!\n", result.ModifiedCount)
			fmt.Println(endTime.Sub(startTime).Seconds())

			value2 = walletAddress
			return value2

		} else if option == 3 {
			var walletName string
			var walletAddress string
			fmt.Println("WalletName:\t")
			fmt.Scan(&walletName)
			fmt.Println("WalletAddress:\t")
			fmt.Scan(&walletAddress)

			startTime := time.Now()

			result, err := collection.UpdateOne(
				context.Background(),
				bson.D{{"walletAddress", value}},
				bson.D{{"$set", bson.D{{"walletName", walletName},
					{"walletAddress", walletAddress}}}})
			if err != nil {
				log.Fatal(err)
			}
			endTime := time.Now()

			fmt.Printf("Обновленно %v Документов!\n", result.ModifiedCount)
			fmt.Println(endTime.Sub(startTime).Seconds())

			value2 = walletAddress
			return value2
		}
		fmt.Scan(&option)
	}
	return value2
}
