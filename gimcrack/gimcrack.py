#!/usr/bin/env python
import argparse
import curses

from game.gimcrack import GimCrack

def usage(args):
    args.app.print_help()

# Parser Command line args
parser = argparse.ArgumentParser(
    description="GimCrack"
)
parser.set_defaults(func=usage, app=parser)

# Required Arguments
parser.add_argument("rows", type=int)
parser.add_argument("cols", type=int)

# Options
parser.add_argument("--moves", "-m",
    type=int, default=25, help="Number of moves")

parser.add_argument("--delay", "-d",
    type=float, default=0.25, help="Delay between moves")

args = parser.parse_args()

def main(stdscr, args):
    # Create and Run
    game = GimCrack(
        stdscr,
        args.rows, args.cols,
        moves=args.moves,
        delay=args.delay
    )
    game.play()
    stdscr.addstr("|--Any Key to Exit--", curses.A_REVERSE)
    stdscr.getch()

curses.wrapper(main, args)
