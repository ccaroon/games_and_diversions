#!/usr/bin/env python
import time
import math

class Astro:
    # PI = 3.1415926535897932384626433832795
    RAD = math.pi / 180.0
    SMALL_FLOAT = 1e-12

    #******************************************************************************/
    #* Returns the number of julian days for the specified day.*/
    #******************************************************************************/
    def julian_date(year:int, month:int, day:int) -> float:
        if month < 3:
            year -= 1
            month += 12

        A = math.floor(year/100.00)
        B = math.floor(A/4.0)
        C = 2-A+B
        E = math.floor(365.25*(year+4716))
        F = math.floor(30.6001*(month+1))
        julian_date = C+day+E+F-1524.5

        return julian_date

    def sun_position(julian_date:float) -> float:
        n = 360.0 / 365.2422 * julian_date
        i = n // 360
        n = n - i * 360.0
        x = n - 3.762863

        x = x + 360 if x < 0 else x
        x *= Astro.RAD
        e = x

        while True:
            dl = e - .016718 * math.sin(e) - x
            e = e - dl / (1 - .016718 * math.cos(e))
            if math.fabs(dl) < Astro.SMALL_FLOAT:
                break

        v = 360 / math.pi * math.atan(1.01686011182 * math.tan(e / 2))
        l = v + 282.596403
        i = l // 360
        l = l - i * 360.0

        return l



if __name__ == "__main__":
    now = time.localtime()
    print(f"{now.tm_mon}/{now.tm_mday}/{now.tm_year}")

    jd = Astro.julian_date(now.tm_year, now.tm_mon, now.tm_mday)
    print(f"Julian Date [{jd}]")

    sun_pos = Astro.sun_position(jd)
    print(f"Sun Pos [{sun_pos}]")













#
