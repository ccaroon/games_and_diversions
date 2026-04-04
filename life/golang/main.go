package main

import (
	"fmt"
	"game_of_life/gol"
	"log"
	"os"

	gc "github.com/rthornton128/goncurses"
	"github.com/spf13/cobra"
)

func gameOfLife(alive, dead rune, patternFile string, maxGens int16, delay int16) {
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

	gol := gol.New(stdscr, alive, dead, patternFile, maxGens, delay)
	gol.Run()
}

func main() {
	var delayFlag int16
	var maxGenFlag int16
	var aliveFlag string
	var deadFlag string
	var patternFlag string

	rootCmd := &cobra.Command{
		Use:   "game_of_life",
		Short: "Conway's Game of Life",
		// Args:  cobra.ExactArgs(2),
		Run: func(cmd *cobra.Command, args []string) {
			gameOfLife(rune(aliveFlag[0]), rune(deadFlag[0]), patternFlag, maxGenFlag, delayFlag)
		},
	}
	rootCmd.Flags().Int16VarP(&delayFlag, "delay", "D", 250, "Delay Between Generations")
	rootCmd.Flags().Int16VarP(&maxGenFlag, "gens", "g", 100, "Max Generations to Simulate")
	rootCmd.Flags().StringVarP(&aliveFlag, "alive", "a", "*", "Symbol for Live Cells")
	rootCmd.Flags().StringVarP(&deadFlag, "dead", "d", " ", "Symbol for Dead Cells")
	rootCmd.Flags().StringVarP(&patternFlag, "pattern", "p", "", "Seed with predefined pattern")

	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

}
