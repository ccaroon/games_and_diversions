#!/usr/bin/env python
import argparse
import curses

from boids.simulation import Simulation

def main(stdscr, args):
    boids = Simulation(
        stdscr,
        args.count,
        iterations=args.iterations,
        delay=args.delay,
        marker=args.marker,
        debug=args.debug
    )
    boids.run()

    stdscr.addstr("--Any Key to Exit--", curses.A_REVERSE)
    stdscr.nodelay(False)
    stdscr.getch()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Boids - Flocking Simulation"
    )
    parser.add_argument("--count", "-c", type=int, default=10, required=False, help="Number of Boids")
    parser.add_argument("--iterations", "-i", type=int, default=100, required=False, help="Number of iterations to run")
    parser.add_argument("--delay", "-d", type=float, default=0.10, required=False, help="Delay between iterations")
    parser.add_argument("--marker", "-m", type=str, default="·", required=False, help="Character to use as Boid marker")
    parser.add_argument("--debug", action='store_true', help="Turn on debugging")

    args = parser.parse_args()

    curses.wrapper(main, args)
# ·
# ●
