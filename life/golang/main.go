package main

import (
	"fmt"
	"game_of_life/gol"
	"log"
	"os"

	gc "github.com/rthornton128/goncurses"
	"github.com/spf13/cobra"
)

func gameOfLife(alive, dead rune, maxGens int16, delay int16) {
	stdscr, err := gc.Init()
	if err != nil {
		log.Fatal("init", err)
	}
	defer gc.End()

	if !gc.HasColors() {
		log.Fatal("Colors not supported!")
	}

	if err := gc.StartColor(); err != nil {
		log.Fatal(err)
	}

	gc.Raw(true)   // turn on raw "uncooked" input
	gc.Echo(false) // turn echoing of typed characters off
	gc.Cursor(0)   // hide cursor

	gol := gol.New(stdscr, alive, dead, maxGens, delay)
	gol.Run()
}

func main() {
	var delay int16
	var maxGens int16
	var alive string
	var dead string

	rootCmd := &cobra.Command{
		Use:   "game_of_life",
		Short: "Conway's Game of Life",
		// Args:  cobra.ExactArgs(2),
		Run: func(cmd *cobra.Command, args []string) {
			gameOfLife(rune(alive[0]), rune(dead[0]), maxGens, delay)
		},
	}
	rootCmd.Flags().Int16VarP(&delay, "delay", "D", 250, "Delay Between Generations")
	rootCmd.Flags().Int16VarP(&maxGens, "gens", "g", 100, "Max Generations to Simulate")
	rootCmd.Flags().StringVarP(&alive, "alive", "a", "*", "Symbol for Live Cells")
	rootCmd.Flags().StringVarP(&dead, "dead", "d", " ", "Symbol for Dead Cells")

	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

}
