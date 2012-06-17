import datetime, re

def active_mods(data):
    d = {}
    for point in data:
        mod = point['mod']
        if not d.has_key(mod):
            d[mod] = 1
        else:
            d[mod] += 1
    return d

def modreqs_per_day(data, limit):
    times = {}
    points = []

    for point in data:
        reqTime = datetime.date.fromtimestamp(point['time']/1000)
        today = datetime.date.today()
        margin = datetime.timedelta(days = limit)
        if today - margin <= reqTime <= today + margin:
            reqTime = datetime.date.today() - reqTime
            reqTime = re.sub("[^0-9]", "", str(reqTime)[:2])
            if not times.has_key(reqTime):
                times[reqTime] = 1
            else:
                times[reqTime] += 1

    for key in times:
        points.append(times[key])

    return points