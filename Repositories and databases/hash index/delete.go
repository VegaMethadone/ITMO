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
	// Задаем контекст при подключение, который, если выполняет, подключение закрывается (лимит 300 секунд)
	ctx, _ := context.WithTimeout(context.Background(), 300*time.Second)
	err = client.Connect(ctx)
	// Если наша ошибка не равна nil - это значит, что что-то пошло не так и переменная err будет содержать эту ошибку
	if err != nil {
		log.Fatal(err)
	}
	// Закрываем подключение к нашей базе данных в конце все функции Delete
	// Переменная с ключевым словом defer выполняется в конце программы
	defer client.Disconnect(ctx)

	// Объявляем коллекцию, которая хранит в себе путь к БД и коллекции БД
	collection := client.Database("Laba").Collection("Wallets")

	// Удаляем документ из нашей коллекции
	result, err := collection.DeleteOne(context.Background(),
		bson.D{{"walletAddress", arr[index]}})
	// Если ошибка не nil, выводим логи ошибки
	if err != nil {
		log.Fatal(err)
	}

	// Объявляем, что наш массив под выбранным индексом будет равен nil вместо адресса
	arr[index] = "nil"
	//Добавляем индекс ячейки нашего массива в массив ячеек nil.
	// Example: ["0x00000000219ab540356cBB839Cbe05303d7705Fa", "nil", "0xDA9dfA130Df4dE4673b89022EE50ff26f6EA73Cf", "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"]
	freeCells = append(freeCells, index)

	fmt.Printf("Удаленно %v Документов!\n", result.DeletedCount)

	return arr, freeCells
}
