import utime

# ISO8601 "2025-11-30T00:46:34.909Z" → timestamp Unix (en secondes)
def iso_to_unix(ts):
    ts = ts.rstrip("Z")
    if "." in ts:
        ts = ts.split(".")[0]

    date, time_ = ts.split("T")
    year, month, day = map(int, date.split("-"))
    hour, minute, second = map(int, time_.split(":"))
    return utime.mktime((year, month, day, hour, minute, second, 0, 0))