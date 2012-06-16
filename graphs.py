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
    tempTimes = []
    times = {}
    points = []

    for point in data:
        reqTime = datetime.date.fromtimestamp(point['time']/1000)
        today = datetime.date.today()
        margin = datetime.timedelta(days = limit)
        if today - margin <= reqTime <= today + margin:
            tempTimes.append(reqTime)

    for time in tempTimes:
        time = datetime.date.today() - time
        time = re.sub("[^0-9]", "", str(time)[:2])
        if not times.has_key(time):
            times[time] = 1
        else:
            times[time] += 1
    for key in times:
        points.append(times[key])

    return points