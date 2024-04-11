#!/usr/bin/env python
import argparse
import curses
import random

from antz.simulation import AntzSimulation

def main(stdscr, args):
    simulation = AntzSimulation(
        stdscr,
        count=args.count,
        day_len=args.day_length,
        max_days=args.max_days,
        ant_marker=args.ant,
        trail_marker=args.trail,
        camp_marker=args.camp,
        debug=args.debug
    )
    simulation.run()

    stdscr.addstr("--Any Key to Exit--", curses.A_REVERSE)
    stdscr.nodelay(False)
    stdscr.getch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Antz - Two Ants, Lost in the Big, Wide World...Searching for one another!"
    )
    parser.add_argument("--count", "-c", type=int, default=2, required=False, help="Number of Antz")
    # parser.add_argument("--iterations", "-i", type=int, default=250, required=False, help="Number of iterations to run")
    parser.add_argument("--day-length", "-d", type=float, default=0.10, required=False, help="Length of 1 day (iteration)")
    parser.add_argument("--max-days", "-i", type=int, default=500, required=False, help="Max number of days (Max Iterations)")
    parser.add_argument("--ant", "-a", type=str, default="⊙", required=False, help="Ant Marker")
    parser.add_argument("--trail", "-t", type=str, default="·", required=False, help="Trail Marker")
    parser.add_argument("--camp", "-m", type=str, default="●", required=False, help="Camp Marker")
    parser.add_argument("--debug", action='store_true', help="Turn on debugging")

    args = parser.parse_args()

    curses.wrapper(main, args)
