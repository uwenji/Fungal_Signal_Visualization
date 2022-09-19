import math 

def Distance(from_x, from_y, to_x, to_y):
    return math.sqrt(math.pow(to_x - from_x) + math.pow(to_y - from_y))

def Rgb2Hex(r, g, b):
  return '#'+('{:X}{:X}{:X}').format(r, g, b)

def ColorGradient(value, colorA, colorB):
    red = (colorB['R'] - colorA['R'])*value + colorA['R']
    green = (colorB['G'] - colorA['G'])*value + colorA['G']
    blue = (colorB['B'] - colorA['B'])*value + colorA['B']
    return  {'R':red, 'G':green, 'B':blue}

ColorA = {'R':124, 'G':180, 'B':255}
ColorB = {'R':90, 'G':255, 'B':255}

myLocation = (16,0)
mid_points = [] # input
hexDict = [] #grid
maxDistance = 0.0
for i in range(len(mid_points)):
    #the point(x, y) => x is point[0], y is point[1]
    #dict structure is {distance, }
    value = Distance(myLocation[0], myLocation[1], mid_points[i][0], mid_points[i][1])
    if(maxDistance < value):
        maxDistance = value
    eachDict = {
        "id": i,
        "dictance":value,
        "color": "#0066ff",
        }
    hexDict.append(eachDict)

for strip in hexDict:
    color = ColorGradient(strip["dictance"]/maxDistance, ColorA, ColorB)
    hex = Rgb2Hex(color['R'], color['G'], color['B'])
    strip["color"] = hex


    