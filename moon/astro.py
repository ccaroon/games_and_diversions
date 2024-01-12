import math

RAD = math.pi / 180.0
SMALL_FLOAT = 1e-12

#******************************************************************************/
#* Returns the number of julian days for the specified day.*/
#******************************************************************************/
def julian_date(year:int, month:int, day:float) -> float:
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
    x *= RAD
    e = x

    while True:
        dl = e - .016718 * math.sin(e) - x
        e = e - dl / (1 - .016718 * math.cos(e))
        if math.fabs(dl) < SMALL_FLOAT:
            break

    v = 360 / math.pi * math.atan(1.01686011182 * math.tan(e / 2))
    l = v + 282.596403
    i = l // 360
    l = l - i * 360.0

    return l

def moon_position(julian_date:float, sun_pos:float):
    ms = 0.985647332099*julian_date - 3.762863

    if ms < 0:
        ms += 360.0

    l = 13.176396*julian_date + 64.975464
    i = l // 360
    l = l - i * 360.0

    if l < 0:
        l += 360.0

    mm = l - 0.1114041 * julian_date - 349.383063
    i = mm // 360
    mm -= i * 360.0
    n = 151.950429 - 0.0529539 * julian_date
    i = n // 360
    n -= i * 360.0
    ev = 1.2739 * math.sin((2*(l-sun_pos)-mm)*RAD)
    sms = math.sin(ms*RAD)
    ae = 0.1858*sms
    mm += ev-ae- 0.37*sms
    ec = 6.2886*math.sin(mm*RAD)
    l += ev + ec - ae + 0.214 * math.sin(2*mm*RAD)
    l = 0.6583 * math.sin(2*(l-sun_pos)*RAD) + l

    return l

def moon_illum(year, month, day, hour):
    """ Return the Moon's Illumination as a Percetage """
    jd  = julian_date(year, month, float(day) + float(hour) / 24.0) - 2444238.5
    sun_pos = sun_position(jd)
    moon_pos = moon_position(jd, sun_pos);

    t = moon_pos - sun_pos
    if t < 0:
        t += 360

    moon_x = (1.0 - math.cos((moon_pos - sun_pos) * RAD)) / 2

    return math.floor(moon_x * 1000.0 + 0.5) / 10
