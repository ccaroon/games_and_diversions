#!/usr/bin/env python
import argparse
import curses

from game_of_life.game_of_life import GameOfLife

def usage(args):
    args.app.print_help()

# Parser Command line args
parser = argparse.ArgumentParser(
    description="Conway's Game of Life"
)
parser.set_defaults(func=usage, app=parser)

# Required Arguments
parser.add_argument("width", type=int)
parser.add_argument("height", type=int)

# Options
parser.add_argument("--alive",
    type=str, default="●", help="Live cell character")
parser.add_argument("--dead",
    type=str, default=" ", help="Dead cell character")

parser.add_argument("--pattern",
    type=str, default=None, help="Seed pattern: Absolute or relative path OR named pattern in patterns/ dir.")

parser.add_argument("--seed-percent", "-p",
    type=int, default=50, help="Percentage of board to seed with live cells when randomly seeding.")

parser.add_argument("--generations", "-g",
    type=int, default=50, help="Number of generations")

parser.add_argument("--delay", "-d",
    type=float, default=0.25, help="Delay between generations")

parser.add_argument("--wrap", "-w",
    action='store_true', help="Wrap edges instead of clipping")

args = parser.parse_args()

def main(stdscr, args):
    # Create and Run
    game = GameOfLife(
        stdscr,
        args.width, args.height,
        alive=args.alive, dead=args.dead,
        pattern=args.pattern,
        seed_percent=args.seed_percent,
        max_gens=args.generations,
        delay=args.delay,
        wrap_edges=args.wrap
    )
    game.run()
    stdscr.addstr("|--Any Key to Exit--", curses.A_REVERSE)
    stdscr.getch()

curses.wrapper(main, args)
