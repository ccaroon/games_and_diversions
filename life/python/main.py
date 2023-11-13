#!/usr/bin/env python
import argparse

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
    type=str, default="*", help="Live cell character")
parser.add_argument("--dead",
    type=str, default=" ", help="Dead cell character")

parser.add_argument("--generations", "-g", 
    type=int, default=25, help="Number of generations")

parser.add_argument("--delay", "-d", 
    type=float, default=0.5, help="Delay between generations")

args = parser.parse_args()

# Create and Run
game = GameOfLife(
    args.width, args.height, 
    alive=args.alive, dead=args.dead,
    max_gens=args.generations
)
game.run(delay=args.delay)
