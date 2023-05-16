package main

import (
	"encoding/json"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	_ "github.com/lib/pq"
	"log"
	"os"
	"strings"
)

type Person struct {
	// Объявляю структуру person, в которой буду нормализировать данные
	ID        int
	WalletId  int
	FirstName string
	LastName  string
	Country   string
	City      string
	District  string
}

// Функция чекер, которая проверяет наличие невалидных символов и удаляет их из набора данных
func checker(str string, symbols []string) string {

	for i := 0; i < len(symbols); i++ {
		str = strings.ReplaceAll(str, symbols[i], "")
	}

	return str
}

func Transform(person Person, wallet Wallet) (Person, Wallet) {
	// Эта функция отвечает за трансформация самих данных
	// получает на вход две переменных типа person & wallet
	// Возвращает уже нормализованные данные

	p := person
	p.FirstName = checker(p.FirstName, Symbols)
	p.LastName = checker(p.LastName, Symbols)
	p.Country = checker(p.Country, Symbols)
	p.City = checker(p.City, Symbols)
	p.District = checker(p.District, Symbols)

	w := wallet
	w.WallerAddress = checker(w.WallerAddress, Symbols)
	w.WalletInfo.Currency = checker(w.WalletInfo.Currency, Symbols)

	return p, w
}

func ETL(person []Person, wallet []Wallet) ([]Person, []Wallet) {
	// Функция отвечает за преобразование самих данных и создание мета файла оперативных данных

	// Объяыляю массив данных, которые позже будут добавлены в json файл как МетаДанные
	var data []MetaData

	// Так как у нас данные связанны друг с другом и в теории у нас в MySQL лежит тоже самое колличество данных как и в Mongo, поэтоу итеррируемся в длину wallet
	for i := 0; i < len(wallet); i++ {

		// Тут идет процесс записи элемента элемента файла мета данных
		// Структура будущего файла лежит в файле metaJson.go

		// Запоминаем преобразованные данные, чтобы потом с ними в конце работать
		tmpPerson, tmpWallet := Transform(person[i], wallet[i])

		// преобразованные данные из Mongo в Postgres
		postgresDataWallet := PostgresDataWallet{
			WalletAddress: tmpWallet.WallerAddress,
			WalletId:      tmpWallet.WalletID,
			Currency:      tmpWallet.WalletInfo.Currency,
			Amount:        tmpWallet.WalletInfo.Amount,
			AmountUsd:     tmpWallet.WalletInfo.AmountUsd,
		}

		// Преобразованные данные из MySql в Postgres
		postgresDataPerson := PostgresDataPerson{
			WalletId:  tmpPerson.WalletId,
			FirstName: tmpPerson.FirstName,
			LastName:  tmpPerson.LastName,
			Country:   tmpPerson.Country,
			City:      tmpPerson.City,
			District:  tmpPerson.District,
		}

		// Складываем данные в Postgres
		postgresDataInfo := PostgresDataInfo{
			PostgresDataPerson: []PostgresDataPerson{postgresDataPerson},
			PostgresDataWallet: []PostgresDataWallet{postgresDataWallet},
		}

		// Вложенные данные из Mongo
		mongoDataWalletInfo := MongoDataWalletInfo{
			Currency:  wallet[i].WalletInfo.Currency,
			Amount:    wallet[i].WalletInfo.Amount,
			AmountUsd: wallet[i].WalletInfo.AmountUsd,
		}

		// Данные из Mongo с вложенными данными
		mongoDataWallet := MongoDataWallet{
			WalletAddress:       wallet[i].WallerAddress,
			WalletId:            wallet[i].WalletID,
			MongoDataWalletInfo: []MongoDataWalletInfo{mongoDataWalletInfo},
		}

		// Данные из MySql
		mySqlDataPerson := MySqlDataPerson{
			MySqlId:   person[i].ID,
			WalletId:  person[i].WalletId,
			FirstName: person[i].FirstName,
			LastName:  person[i].LastName,
			Country:   person[i].Country,
			City:      person[i].City,
			District:  person[i].District,
		}

		// Финальная структура со всеми данными сверху
		newData := MetaData{
			MySqlId:          person[i].ID,
			MongoId:          wallet[i].ID,
			PostgresId:       person[i].ID,
			MySqlDataPerson:  []MySqlDataPerson{mySqlDataPerson},
			MongoDataWallet:  []MongoDataWallet{mongoDataWallet},
			PostgresDataInfo: []PostgresDataInfo{postgresDataInfo},
		}

		data = append(data, newData)

		// Переписываем изначальные элементы массивов на обработанные данные
		person[i], wallet[i] = tmpPerson, tmpWallet
	}

	// Преобразование данных в формат json
	jsonData, err := json.MarshalIndent(data, "", "\t")
	if err != nil {
		log.Fatal(err)
	}

	// Создание файла и запись на файл
	err = os.WriteFile("meta.json", jsonData, 0644)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Print("JSON записан в Файле meta.json")

	return person, wallet
}
