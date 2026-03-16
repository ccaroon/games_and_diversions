package main

import (
	"game_of_life/gol"
	"log"

	gc "github.com/rthornton128/goncurses"
)

func curses() {
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
	// stdscr.Keypad(true)   // allow keypad input

	height, width := stdscr.MaxYX()

	colorIdx := int16(1)
	stdscr.ColorOn(colorIdx)
	stdscr.Printf("W[%d] | H[%d]\n", width, height)
	stdscr.Println("Hello, World!")
	stdscr.ColorOff(colorIdx)
	stdscr.Refresh()

	// if ch := stdscr.GetChar(); ch == gc.KEY_F2 {
	// 	stdscr.Print("The F2 key was pressed.")
	// } else {
	// 	stdscr.Print("The key pressed is: ")
	// 	stdscr.AttrOn(gc.A_BOLD)
	// 	stdscr.AddChar(gc.Char(ch))
	// 	stdscr.AttrOff(gc.A_BOLD)
	// }
	// stdscr.Refresh()
	stdscr.GetChar()
}

func main() {
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

	gol := gol.New(stdscr)
	gol.Run()
}
