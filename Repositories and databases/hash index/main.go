package main

import "fmt"

func main() {
	// Выводим доступные опции
	fmt.Println("Выбери опцию:\n 1)Сгенерировать данные\n 2)Сделать Хеш-Индексы\n 3)Найти по Хеш-Индексу\n 4)Удалить данные\n 5)Добавить данные\n 6)Обновить данные\n 0)Выход")
	// Объявляем массив, который будет хранить наши адреса
	var arr = []string{}
	// Массив, который будет хранить свободные ячейки после удаления данных  из массива выше
	var freeCells = []int{}

	// Объявляем и считываем переменную выбора действия
	var option int
	fmt.Scan(&option)
	for option != 0 {
		if option == 1 {
			// Задаем количество документов, которое должно быть сгенерированно
			var n int
			fmt.Scan(&n)
			AddData(n)
		}
		if option == 2 {
			// Создаем Хеш-Индексы
			arr = HashIndex()
		}
		if option == 3 {
			// Обращаемся к файловой надстройке и выводим n-тый индекс
			var n int
			fmt.Scan(&n)
			value := arr[n]
			// Проыеряем, существкет ли наш n-тый идекс
			if value == "nil" {
				fmt.Println("Нет кошелька с таким индексом")
			} else {
				// Иначе ищим в файле наш индекс
				FindData(value)
			}
		}
		if option == 4 {
			// Считываем индекс, заменяем значение адреса на nil
			var index int
			fmt.Scan(&index)
			arr, freeCells = Delete(arr, freeCells, index)
			if len(freeCells) != 0 {
				// Если длина массива свободных ячеек != 0  - выводим их
				for i := 0; i < len(freeCells); i++ {
					fmt.Print(freeCells[i], " ")
				}
			} else {
				fmt.Println("FreeCells пуст")
			}
		}
		if option == 5 {
			// Тоже самое, что и добавление из 1 варианта, только вручную
			value := AddByHand()
			if len(freeCells) != 0 {
				var index int
				index = freeCells[0]
				arr[index] = value
				freeCells = freeCells[0:]
			} else {
				arr = append(arr, value)
			}
		}
		if option == 6 {
			// Обнавление документа и файловой надстройки
			var index int
			fmt.Println("Какой индекс кошелька ?")
			fmt.Scan(&index)
			// Проверяем, существует ли данный индекс
			if index > len(arr) {
				fmt.Println("Неверный индекс")
			} else {
				newValue := Update(arr[index])
				arr[index] = newValue
			}
		}
		fmt.Println("Выбери опцию:\n 1)Сгенерировать данные\n 2)Сделать Хеш-Индексы\n 3)Найти по Хеш-Индексу\n 4)Удалить данные\n 5)Добавить данные\n 6)Обновить данные\n 0)Выход")
		fmt.Scan(&option)
	}
}
