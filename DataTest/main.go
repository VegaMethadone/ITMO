package main

import (
	"encoding/json"
	"fmt"
	"github.com/jaswdr/faker"
	"io/ioutil"
	"log"
	"math/rand"
	"os"
	"strconv"
)

type Person struct {
	Name    string `json:"name"`
	Age     int    `json:"age"`
	Address string `json:"address"`
}

func jsonCreation(n int) {
	file, err := os.Create("meta.json")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	for i := 0; i < n; i++ {
		person := map[string]interface{}{
			"wallet": map[string]string{
				"name":    faker.New().Person().Name(),
				"age":     strconv.Itoa(rand.Int() % 100),
				"address": faker.New().Address().Address(),
			},
		}

		data, err := json.MarshalIndent(person, "", "    ")
		if err != nil {
			log.Fatal(err)
		}

		err = ioutil.WriteFile("wallet.json", data, 0644)
		if err != nil {
			log.Fatal(err)
		}
		/*encoder := json.NewEncoder(file)
		err = encoder.Encode(string(data))
		if err != nil {
			log.Fatal(err)
		}

		*/
	}

	fmt.Print("JSON записан в Файле meta.json")
}

func jsonBeauty(n int) {
	birds := map[string]interface{}{
		"sounds": map[string]string{
			"pigeon":  "coo",
			"eagle":   "squak",
			"owl":     "hoot",
			"duck":    "quack",
			"cuckoo":  "ku-ku",
			"raven":   "cruck-cruck",
			"chicken": "cluck",
			"rooster": "cock-a-doodle-do",
		},
	}

	data, err := json.MarshalIndent(birds, "", "    ")

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(string(data))
}
