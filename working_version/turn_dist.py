import math
from geopy import distance


class Coordinate:
    def __init__(self,lat, lon):
        self.lat = lat
        self.lon = lon





def distance_check(x,y):
    new_x = (x.lat, x.lon)
    new_y = (y.lat, y.lon)
    dist = distance.distance(new_x,new_y)
    return dist





def turn(x,y,z):
    if z.lon >= y.lon:
        if x.lat >= y.lat:
            return "left"
        else:
            return "right"
    else:
        if x.lat >= y.lat:
            return "right"
        else:
            return "left"
    if z.lat >= y.lat:
        if x.lon >= y.lon:
            return "right"
        else:
            return "left"
    else:
        if x.lon >= y.lon:
            return "left"
        else:
            return "right"

    



c1 = Coordinate(44.587502, -123.262497)
c2 = Coordinate(44.587414, -123.262405)
c3 = Coordinate(44.587559, -123.262489)
print(turn(c1,c2,c3))
c4 = Coordinate(44.612461, -123.26223)
c5 = Coordinate(44.612705, -123.262794)
c6 = Coordinate(44.612736, -123.263123)
print(turn(c4,c5,c6))
val = (c1.lat, c1.lon)
val2 = (c2.lat, c2.lon)
print(distance_check(c1, c2))
print(distance_check(c1, c4))
