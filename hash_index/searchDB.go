package main

import (
	"fmt"
	"time"
)

func SearchData(x int) LabSet {
	startTime := time.Now()

	arr := MapSet()
	result := arr[x]
	fmt.Println(result)

	endTime := time.Now()
	fmt.Println(endTime.Sub(startTime).Seconds())

	return result
}
