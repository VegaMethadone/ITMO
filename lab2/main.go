package main

import "fmt"

var Global int = 0

func main() {
	fmt.Println("Выбери опцию:\n 1)Сгенерировать данные\n 2)Сделать Хеш-Индексы\n 3)Найти по Хеш-Индексу\n 4)Удалить данные\n 5)Добавить данные\n 6)Обновить данные\n 0)Выход")
	var arr = []string{}
	var freeCells = []int{}

	var option int
	fmt.Scan(&option)
	for option != 0 {
		if option == 1 {
			var n int
			fmt.Scan(&n)
			AddData(n)
		}
		if option == 2 {
			arr = HashIndex()
		}
		if option == 3 {
			var n int
			fmt.Scan(&n)
			value := arr[n]
			if value == "nil" {
				fmt.Println("Нет кошелька с таким индексом")
			} else {
				FindData(value)
			}
		}
		if option == 4 {
			var index int
			fmt.Scan(&index)
			arr, freeCells = Delete(arr, freeCells, index)
			if len(freeCells) != 0 {
				for i := 0; i < len(freeCells); i++ {
					fmt.Print(freeCells[i], " ")
				}
			} else {
				fmt.Println("FreeCells пуст")
			}
		}
		if option == 5 {
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
			var index int
			fmt.Println("Какой индекс кошелька ?")
			fmt.Scan(&index)
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
