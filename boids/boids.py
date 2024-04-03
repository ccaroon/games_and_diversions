#!/usr/bin/env python
import argparse
import curses

from boids.simulation import Simulation

def main(stdscr, args):
    boids = Simulation(stdscr, args.count)
    boids.run()

    stdscr.addstr(curses.LINES-1, 0, "|--Any Key to Exit--", curses.A_REVERSE)
    stdscr.getch()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Boids - Flocking Simulation"
    )
    parser.add_argument("--count", type=int, default=10, required=False)
    args = parser.parse_args()

    curses.wrapper(main, args)
