package main

import (
	"fmt"
)

func MapSet() map[int]LabSet {
	DataSet := make(map[int]LabSet)
	return DataSet
}

func main() {
	fmt.Println("Choose  option: \n 1)\tAdd data \n 2)\tShow data \n 3)\tHash && Search \n 0)\tExit")
	var option int8
	fmt.Scan(&option)
	for option != 0 {
		switch option {
		case 1:
			var num int
			fmt.Scan(&num)
			FillDatabase(num)
		case 2:
			ReadDB()
		case 3:
			HashData()
		case 4:
			var x int
			fmt.Scan(&x)
			SearchData(x)
		case 0:
			return
		}
		fmt.Println("Choose  option: \n 1)\tAdd data \n 2)\tShow data \n 3)\tHash data \n 0)\tExit")
		fmt.Scan(&option)
	}
}
