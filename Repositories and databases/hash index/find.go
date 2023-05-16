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

func FindData(value string) {

	// Подключение к базе данных
	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://localhost:27017"))
	// Вывод ошибки в случае err будет содержать в себе значение, отличное от nil
	if err != nil {
		log.Fatal(err)
	}

	//Задаем контекст подключниея, в случае которого мы отключяимся от БД (TimeLimit 300 sec)
	ctx, _ := context.WithTimeout(context.Background(), 300*time.Second)
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}

	// В конце программы обязательно закрыть подключние к БД
	defer client.Disconnect(ctx)

	collection := client.Database("Laba").Collection("Wallets")

	// Создаем филтьр для поиска нужной записи и передаем нашего значение из надстройки
	filter := bson.D{{"walletAddress", value}}

	startTime := time.Now()

	// Находим нужное значение в файле, декодируем его и присваем переменной result
	var result bson.D
	err = collection.FindOne(context.TODO(), filter).Decode(&result)
	if err != nil {
		log.Fatal(err)
	}
	endTime := time.Now()
	fmt.Println(endTime.Sub(startTime).Seconds())
	fmt.Println(result)
}

/*
func main() {
	startTime := time.Now()
	FindData("0xy8VBhkh79010HcR22fny0PYXK7G7YJ9cA7f9Ro9W")
	endTime := time.Now()

	fmt.Println(endTime.Sub(startTime).Seconds())
}
*/
