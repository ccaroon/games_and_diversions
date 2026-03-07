package main

import (
	"fmt"
	"strconv"
)

func digitalRoot(number int) int {
	var dRoot int

	if number <= 9 {
		dRoot = number
	} else {
		// add up all the digits
		// 1. turn number into string
		numStr := strconv.Itoa(number)

		// 2. iterate over each char
		total := 0
		for idx := range numStr {
			// 3. char to int and add to total
			digit, err := strconv.Atoi(string(numStr[idx]))
			if err != nil {
				panic(err)
			}
			total += digit
		}

		// if total > 9, recurse
		if total > 9 {
			dRoot = digitalRoot(total)
		} else {
			dRoot = total
		}
	}

	return dRoot
}

func main() {
	// fmt.Println(digitalRoot(7))
	// fmt.Println(digitalRoot(1234567890))

	for number := range 1_000 {
		fmt.Printf("%d) %d\n", number, digitalRoot(number))
	}

}
