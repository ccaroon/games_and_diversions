#!/usr/bin/env python
import math
import time

import astro

if __name__ == "__main__":
    now = time.localtime()
    print(f"{now.tm_mon}/{now.tm_mday}/{now.tm_year}")

    jd = astro.julian_date(now.tm_year, now.tm_mon, now.tm_mday)
    print(f"Julian Date [{jd}]")

    sun_pos = astro.sun_position(jd)
    print(f"Sun Pos [{sun_pos}]")

    moon_pos = astro.moon_position(jd, sun_pos)
    print(f"Moon Pos [{moon_pos}]")

    moon_illum = astro.moon_illum(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour)
    print(f"Moon Illum: {moon_illum}%")
