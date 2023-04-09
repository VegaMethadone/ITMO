package main

import "go.mongodb.org/mongo-driver/bson/primitive"

type MetaData struct {
	MySqlId          int                `json:"my_sql_id"`
	MongoId          primitive.ObjectID `json:"mongo_id"`
	PostgresId       int                `json:"postgres_id"`
	MySqlDataPerson  []MySqlDataPerson  `json:"my_sql_data_person"`
	MongoDataWallet  []MongoDataWallet  `json:"mongo_data_wallet"`
	PostgresDataInfo []PostgresDataInfo `json:"postgres_data_info"`
}

type MySqlDataPerson struct {
	MySqlId   int    `json:"my_sql_id"`
	WalletId  int    `json:"wallet_id"`
	FirstName string `json:"first_name"`
	LastName  string `json:"last_name"`
	Country   string `json:"country"`
	City      string `json:"city"`
	District  string `json:"district"`
}
type MongoDataWallet struct {
	WalletAddress       string                `json:"wallet_address"`
	WalletId            int                   `json:"wallet_id"`
	MongoDataWalletInfo []MongoDataWalletInfo `json:"mongo_data_wallet_info"`
}
type MongoDataWalletInfo struct {
	Currency  string `json:"currency"`
	Amount    int    `json:"amount"`
	AmountUsd int    `json:"amountUsd"`
}

type PostgresDataInfo struct {
	PostgresDataPerson []PostgresDataPerson `json:"postgres_data_person"`
	PostgresDataWallet []PostgresDataWallet `json:"postgres_data_wallet"`
}
type PostgresDataPerson struct {
	WalletId  int    `json:"wallet_id"`
	FirstName string `json:"first_name"`
	LastName  string `json:"last_name"`
	Country   string `json:"country"`
	City      string `json:"city"`
	District  string `json:"district"`
}
type PostgresDataWallet struct {
	WalletAddress string `json:"walletAddress"`
	WalletId      int    `json:"wallet_id"`
	Currency      string `json:"currency"`
	Amount        int    `json:"amount"`
	AmountUsd     int    `json:"amountUsd"`
}
