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

type LabSet struct {
	Currency         string //`bson:"currency,omitempty"`
	From             string //`bson:"from,omitempty"`
	To               string //`bson:"to,omitempty"`
	TransactionIndex int    //`bson:"transactionIndex,omitempty"`
}

func HashData() { //map[int]LabSet
	// Time count: start
	startTime := time.Now()

	// Define my connection to BD
	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://localhost:27017"))
	if err != nil {
		log.Fatal(err)
	}

	//Define time limit for my connection
	ctx, _ := context.WithTimeout(context.Background(), 300*time.Second)
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}
	// Close my connection in the end of function
	defer client.Disconnect(ctx)

	//Declarate my 1) db name 2) collection name
	startDatabase := client.Database("lab")
	startCollection := startDatabase.Collection("laba")

	// Cursor for iterating in collection

	cursor, cursorErr := startCollection.Find(context.Background(), bson.D{})
	if cursorErr != nil {
		log.Fatal(cursorErr)
	}
	defer cursor.Close(context.Background())

	var arr = make(map[int]LabSet)
	for cursor.Next(context.Background()) {
		res := struct {
			Currency         string
			From             string
			To               string
			TransactionIndex int
		}{}
		cursorErr := cursor.Decode(&res)
		if cursorErr != nil {
			log.Fatal(cursorErr)
		}

		arr[res.TransactionIndex] = res
	}

	endTime := time.Now()
	fmt.Println(endTime.Sub(startTime).Seconds())

	for key, value := range arr {
		fmt.Println("Key:\t", key, "Value:\t", value)
	}

	fmt.Println("\n Search data: \n")
	var findIndex int
	fmt.Scan(&findIndex)

	finalTimeStart := time.Now()
	fmt.Println(arr[findIndex])

	finalTimeEnd := time.Now()
	fmt.Println(finalTimeEnd.Sub(finalTimeStart).Seconds())

	//return arr
}
