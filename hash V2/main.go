package main

import "fmt"

func main() {
	fmt.Println("Выбери опцию:\n 1)Добавить данные\n 2)Сделать Хеш-Индексы\n 3)Найти по Хеш-Индексу\n 0)Выход")
	var arr = []string{}
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
			FindData(value)
		}
		if option == 4 {
			return
		}
		fmt.Println("Выбери опцию:\n 1)Добавить данные\n 2)Сделать Хеш-Индексы\n 3)Найти по Хеш-Индексу\n 0)Выход")
		fmt.Scan(&option)
	}
}
