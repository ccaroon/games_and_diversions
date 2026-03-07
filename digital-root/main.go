package main

import (
	"fmt"
	"os"
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

func printUsage() {
	fmt.Printf("Usage: %s <integer>\n", os.Args[0])
}

func main() {
	if len(os.Args) != 2 {
		printUsage()
	} else {
		number, err := strconv.Atoi(os.Args[1])
		if err != nil {
			fmt.Printf("Invalid Number: '%s'\n", os.Args[1])
		} else {
			fmt.Printf("The Digital Root of [%d] -> [%d]\n", number, digitalRoot(number))
		}
	}
}
