package gol

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"slices"
	"time"

	gc "github.com/rthornton128/goncurses"
)

const colorCell int16 = 1
const colorInfo int16 = 2
const colorDebug int16 = 3

type coord struct {
	x int
	y int
}

var Neighbors [8]coord = [8]coord{
	coord{-1, -1}, coord{+0, -1}, coord{+1, -1},
	coord{-1, +0}, coord{+1, +0},
	coord{-1, +1}, coord{+0, +1}, coord{+1, +1},
}

type gameBoard [][]rune

type GameOfLife struct {
	alive          rune
	dead           rune
	maxGenerations int16
	delay          int16
	wrapEdges      bool
	board1         gameBoard
	board2         gameBoard
	activeBoard    *gameBoard
	bufferBoard    *gameBoard
	width          int
	height         int
	screen         *gc.Window
}

func New(screen *gc.Window, alive, dead rune, patternFile string, maxGens int16, delay int16) *GameOfLife {
	height, width := screen.MaxYX()

	gol := GameOfLife{
		alive:          alive,
		dead:           dead,
		maxGenerations: maxGens,
		delay:          delay,
		wrapEdges:      true,
		width:          width,
		height:         height,
		screen:         screen,
	}

	gol.initBoards()

	if patternFile != "" {
		gol.loadPattern(patternFile)
	} else {
		gol.randomizeBoard()
	}

	gc.InitPair(colorCell, gc.C_GREEN, gc.C_BLACK)
	gc.InitPair(colorInfo, gc.C_BLACK, gc.C_GREEN)
	gc.InitPair(colorDebug, gc.C_RED, gc.C_BLACK)

	return &gol
}

func (gol *GameOfLife) initBoards() {
	// Board 1
	gol.board1 = make(gameBoard, gol.height)
	for ridx := range gol.height {
		gol.board1[ridx] = slices.Repeat([]rune{gol.dead}, gol.width)
	}
	gol.activeBoard = &gol.board1

	// Board 2
	gol.board2 = make(gameBoard, gol.height)
	for ridx := range gol.height {
		gol.board2[ridx] = slices.Repeat([]rune{gol.dead}, gol.width)
	}
	gol.bufferBoard = &gol.board2

}

func (gol *GameOfLife) randomizeBoard() {
	board := *gol.activeBoard

	for ridx := range gol.height {
		for cidx := range gol.width {
			if rand.Intn(100) <= 50 {
				board[ridx][cidx] = gol.alive
			} else {
				board[ridx][cidx] = gol.dead
			}
		}
	}
}

func (gol *GameOfLife) loadPattern(fileName string) {
	fptr, err := os.Open(fileName)
	if err != nil {
		panic(err)
	}
	defer fptr.Close()

	var pattern []string
	scanner := bufio.NewScanner(fptr)
	for scanner.Scan() {
		line := scanner.Text()
		if line[0] != byte('#') {
			pattern = append(pattern, line)
		}
	}

	width := len(pattern[0])
	height := len(pattern)
	startRow := int(gol.height/2 - height/2)
	startCol := int(gol.width/2 - width/2)

	// fmt.Printf("[%dx%d] | (%d,%d)\n", width, height, startRow, startCol)
	// os.Exit(1)

	board := *gol.activeBoard
	for ridx := range height {
		for cidx := range width {
			if pattern[ridx][cidx] == byte('1') {
				board[startRow+ridx][startCol+cidx] = gol.alive
			} else {
				board[startRow+ridx][startCol+cidx] = gol.dead
			}
		}
	}
}

func (gol *GameOfLife) display() {
	board := *gol.activeBoard
	gol.screen.ColorOn(colorCell)
	for cidx := range gol.width {
		for ridx := range gol.height {
			gol.screen.MovePrintf(ridx, cidx, "%c", board[ridx][cidx])
		}
	}
	gol.screen.ColorOff(colorCell)
}

func (gol *GameOfLife) countLiveNeighbors(board *gameBoard, cell coord) int {
	var count int = 0

	for _, offset := range Neighbors {
		nx := cell.x + offset.x
		ny := cell.y + offset.y

		if gol.wrapEdges {
			if nx < 0 {
				nx = gol.width - 1
			} else if nx >= gol.width {
				nx = 0
			}

			if ny < 0 {
				ny = gol.height - 1
			} else if ny >= gol.height {
				ny = 0
			}
		}

		if (nx >= 0 && nx < gol.width) && (ny >= 0 && ny < gol.height) {
			if (*board)[ny][nx] == gol.alive {
				count += 1
			}
		}
	}

	return count
}

func (gol *GameOfLife) setCell(board *gameBoard, cell coord, state rune, count int) {
	x := cell.x
	y := cell.y
	gBoard := *board

	if state == gol.alive {
		if count < 2 {
			// Any live cell with fewer than two live neighbours dies
			gBoard[y][x] = gol.dead
		} else if count == 2 || count == 3 {
			// Any live cell with two or three live neighbours lives
			gBoard[y][x] = gol.alive
		} else if count > 3 {
			// Any live cell with more than three live neighbours dies
			gBoard[y][x] = gol.dead
		}
	} else if state == gol.dead {
		// Any dead cell with exactly three live neighbours becomes a live cell
		if count == 3 {
			gBoard[y][x] = gol.alive

		} else {
			gBoard[y][x] = gol.dead
		}
	}
}

func (gol *GameOfLife) computeNextGen() {
	oldBoard := gol.activeBoard
	newBoard := gol.bufferBoard

	for y := range gol.height {
		for x := range gol.width {
			count := gol.countLiveNeighbors(oldBoard, coord{x, y})
			gol.setCell(newBoard, coord{x, y}, (*oldBoard)[y][x], count)
		}
	}

	// Swap active and buffer/non-active boards
	gol.activeBoard, gol.bufferBoard = gol.bufferBoard, gol.activeBoard
}

func (gol *GameOfLife) updateStatusLine(msg string, clear bool) {
	if clear == true {
		gol.screen.Move(gol.height-1, 0)
		gol.screen.ClearToEOL()
	}

	gol.screen.ColorOn(colorInfo)
	gol.screen.MovePrintf(gol.height-1, 0, "%s", msg)
	gol.screen.ColorOff(colorInfo)
	gol.screen.Refresh()
}

func (gol *GameOfLife) Run() {
	for gen := range gol.maxGenerations {
		gol.display()
		gol.computeNextGen()

		msg := fmt.Sprintf("Game of Life (%dx%d) | Gen #%d/%d", gol.width, gol.height, gen+1, gol.maxGenerations)
		gol.updateStatusLine(msg, false)

		time.Sleep(time.Millisecond * time.Duration(gol.delay))
	}
	gol.updateStatusLine("--Press Any Key to Exit--", true)
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
