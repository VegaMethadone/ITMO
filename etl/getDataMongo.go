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
	ID            primitive.ObjectID `bson:"_id,omitempty"`
	WallerAddress string             `bson:"waller_address"`
	WalletID      int                `bson:"wallet_id"`
	WalletInfo    *WalletInfo        `bson:"wallet_info"`
}

type WalletInfo struct {
	Currency  string `bson:"currency"`
	Amount    int    `bson:"amount"`
	AmountUsd int    `bson:"amountUsd"`
}

func GetDataMongo() []Wallet {
	mongoClient, err := mongo.NewClient(options.Client().ApplyURI("mongodb://localhost:27017"))
	if err != nil {
		log.Fatal(err)
	}

	ctx, _ := context.WithTimeout(context.Background(), 300*time.Second)
	err = mongoClient.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}

	defer mongoClient.Disconnect(ctx)

	collection := mongoClient.Database("Wallets").Collection("Wallet")

	cursor, cursorErr := collection.Find(context.Background(), bson.D{})
	if cursorErr != nil {
		log.Fatal(cursorErr)
	}
	var wallet = []Wallet{}

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
