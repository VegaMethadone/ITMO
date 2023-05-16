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
	//Создание структуры для хешированя данных
	WalletName    string //`bson:"walletName"`
	WalletAddress string //`bson:"walletAddress"`
}

func HashIndex() []string {
	timeStart := time.Now()

	// Подключние к базе данных
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

	cursor, cursorErr := collection.Find(context.Background(), bson.D{})
	if cursorErr != nil {
		log.Fatal(err)
	}

	// Объявление массива, в котором будем хранить наши данные для запроса в файл
	var arr = []string{}

	// Итерируемся по коллекции и извлекаем наши документы
	for cursor.Next(context.Background()) {
		// Объявляем переменную res, которая будет содержать документ и декодируем из bson
		var res wallet
		cursorErr := cursor.Decode(&res)
		if cursorErr != nil {
			log.Fatal(cursorErr)
		}
		// Добавляем наши данные
		arr = append(arr, res.WalletAddress)
	}

	timeEnd := time.Now()
	fmt.Println(timeEnd.Sub(timeStart).Seconds())

	// Тестовая секция, пока не нажмем 0
	var test int
	fmt.Scan(&test)
	for test != 0 {
		fmt.Println(arr[test])
		fmt.Scan(&test)
	}

	return arr
}

/*
func main() {
	arr := HashIndex()
	var x int
	fmt.Scan(&x)
	for x != 0 {
		fmt.Println(arr[x])
		fmt.Scan(&x)
	}
}
*/
