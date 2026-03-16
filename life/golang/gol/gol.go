package gol

import (
	"fmt"
	"math/rand"
	"time"

	gc "github.com/rthornton128/goncurses"
)

const ColorCell int16 = 1
const ColorInfo int16 = 2
const ColorDebug int16 = 3

type offset [2]int

var Neighbors [8]offset = [8]offset{
	offset{-1, -1}, offset{+0, -1}, offset{+1, -1},
	offset{-1, +0}, offset{+1, +0},
	offset{-1, +1}, offset{+0, +1}, offset{+1, +1},
}

type GameOfLife struct {
	alive          rune
	dead           rune
	maxGenerations int
	delay          int64
	board1         [][]rune
	board2         [][]rune
	activeBoard    *[][]rune
	width          int
	height         int
	screen         *gc.Window
}

func New(screen *gc.Window) *GameOfLife {
	height, width := screen.MaxYX()

	gol := GameOfLife{
		alive:          rune('x'),
		dead:           rune(' '),
		maxGenerations: 50,
		delay:          500,
		width:          width,
		height:         height,
		screen:         screen,
	}

	gol.initBoards()
	gol.randomizeBoard()

	gc.InitPair(ColorCell, gc.C_GREEN, gc.C_BLACK)
	gc.InitPair(ColorInfo, gc.C_BLACK, gc.C_GREEN)
	gc.InitPair(ColorDebug, gc.C_RED, gc.C_BLACK)

	return &gol
}

func (gol *GameOfLife) initBoards() {
	// Board 1
	gol.board1 = make([][]rune, gol.height)
	for ridx := range gol.height {
		gol.board1[ridx] = make([]rune, gol.width)
	}

	// Board 2
	gol.board2 = make([][]rune, gol.height)
	for ridx := range gol.height {
		gol.board2[ridx] = make([]rune, gol.width)
	}

	gol.activeBoard = &gol.board1
}

func (gol *GameOfLife) randomizeBoard() {
	board := *gol.activeBoard

	for cidx := range gol.width {
		for ridx := range gol.height {
			if rand.Intn(100) <= 5 {
				board[ridx][cidx] = gol.alive
			} else {
				board[ridx][cidx] = gol.dead
			}
		}
	}
}

func (gol *GameOfLife) display() {
	board := *gol.activeBoard
	gol.screen.ColorOn(ColorCell)
	for cidx := range gol.width {
		for ridx := range gol.height {
			gol.screen.MovePrintf(ridx, cidx, "%c", board[ridx][cidx])
		}
	}
	gol.screen.ColorOff(ColorCell)
}

func (gol *GameOfLife) computeNextGen() {

}

func (gol *GameOfLife) updateStatusLine(gen int) {
	gol.screen.ColorOn(ColorInfo)
	gol.screen.MovePrintf(gol.height-1, 0, "Game of Life | Gen #%d/%d", gen+1, gol.maxGenerations)
	gol.screen.ColorOff(ColorInfo)
	gol.screen.Refresh()
}

func (gol *GameOfLife) Run() {
	for gen := range gol.maxGenerations {
		gol.display()
		gol.computeNextGen()

		gol.updateStatusLine(gen)

		time.Sleep(time.Second / 5)
	}
	gol.screen.GetChar()
}

func (gol *GameOfLife) Print() {
	board := *gol.activeBoard
	for cidx := range gol.width {
		for ridx := range gol.height {
			fmt.Printf("%c ", board[ridx][cidx])
		}
		fmt.Println()
	}
}
