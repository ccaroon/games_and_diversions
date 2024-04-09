#!/usr/bin/env python
import argparse
import curses
import random

# from boids.simulation1 import BoidSimulation1
from boids.simulation2 import BoidSimulation2

def main(stdscr, args):
    boids = BoidSimulation2(
        stdscr,
        args.count,
        iterations=args.iterations,
        delay=args.delay,
        marker=args.marker,
        perch_chance=args.perch_chance,
        trails=args.trails,
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
    parser.add_argument("--count", "-c", type=int, default=random.randint(50, 101), required=False, help="Number of Boids")
    parser.add_argument("--iterations", "-i", type=int, default=250, required=False, help="Number of iterations to run")
    parser.add_argument("--delay", "-d", type=float, default=0.075, required=False, help="Delay between iterations")
    parser.add_argument("--marker", "-m", type=str, default="·", required=False, help="Character to use as Boid marker")
    parser.add_argument("--perch_chance", "-p", type=int, default=random.randint(10,50), required=False, help="Chance that a Boid will stop & perch at ground level")
    parser.add_argument("--trails", "-t", action='store_true', help="Display trails")
    parser.add_argument("--debug", action='store_true', help="Turn on debugging")

    args = parser.parse_args()

    curses.wrapper(main, args)
