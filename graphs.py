import CairoPlot, cairo, datetime, re
              
def donut(data, imagename):
    d = {}
    for point in data:
        mod = point['mod']
        if not d.has_key(mod):
            d[mod] = 1
        else: 
            d[mod] += 1

    CairoPlot.donut_plot(imagename, d, 600, 600, background=(255, 255, 255))

def bar(data, imagename):
    d = {}
    mods = []
    points = []
    total = 0
    for point in data:
        mod = point['mod']
        if not d.has_key(mod):
            d[mod] = 1
        else: 
            d[mod] += 1
    for key in d:
        print key
        mods.append(key)
        points.append(d[key])
        total += d[key]
    vbounds = (total / 2, total)
    CairoPlot.bar_plot (imagename, points, 650, 400, border=20, grid = True, rounded_corners = False, h_labels=mods, background=(255, 255, 255))

def modreqs_per_day(data, imagename):
    
    tempTimes = []
    times = {}
    daysAgo = []
    points = []
    
    for point in data:
        reqTime = datetime.date.fromtimestamp(point['time']/1000)
        
        today = datetime.date.today()
        margin = datetime.timedelta(days = 15)

        if today - margin <= reqTime <= today + margin: tempTimes.append(reqTime)
    for time in tempTimes:
        time = datetime.date.today() - time
        time = re.sub("[^0-9]", "", str(time)[:2])
        if not times.has_key(time):
            times[time] = 1
        else: 
            times[time] += 1
    for key in times:
        daysAgo.append(key)
        points.append(times[key])
        
        
    CairoPlot.dot_line_plot(imagename, points, 600, 400, axis = True, grid = True, background=(255, 255, 255))
