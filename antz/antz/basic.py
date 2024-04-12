#!/usr/bin/env python

from .simulation import AntzSimulation


class AntzBasic(AntzSimulation):
    def __init__(self, **kwargs):
        super().__init__(64, 64, **kwargs)

    def display(self):
        debug_info = "(DEBUG)" if self._debug else ""
        print(f"### | Antz {debug_info} | Day #{self._day}/{self._max_days} | {self._width}x{self._height} | ###")

        for ant in self._antz:
            marker = self._camp_marker if ant.is_camping else self._ant_marker
            print(f"{marker}{ant} {ant.status()}")

    def _process_input(self):
        key = input()
        if key == 'q':
            self._simulation_complete = True
