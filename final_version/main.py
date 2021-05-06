import gpxpy
import requests
import math
import sys
import xlsxwriter
from geopy import distance

sys.setrecursionlimit(1000000)

# Coordinates struct
class Coordinate:
    def __init__(self, lat, lon, add):
        self.lat = lat
        self.lon = lon
        self.address = add


# Function to read coordinates from .gpx file
# and return pairs of (lat, lon)
def read_GPX(filename):
    listOfCoordinates = []
    gpxfile = open(filename, 'r')
    gpx = gpxpy.parse(gpxfile)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                pair = [point.latitude, point.longitude]
                listOfCoordinates.append(pair)
    return listOfCoordinates
    # list = [[long, lat], [x, y], ...]


# Function to request place name based on pair of (lat, lon)
def reverse_Geocoding_streetNameOnly(latitude, longitude, apikey):
    info = {'apiKey': apikey, 'version': 4.10, 'lat': latitude, 'lon': longitude}
    response = requests.get(
        'https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP/default.aspx', params=info)
    string = response.content.decode('utf-8')
    list = string.split(',')
    address = "{0}".format(list[5])
    return address


# Function to reduce the size of list
# Delete unnecessary coordinates
def reduce_Coordinates(listpair, tolerance):
    reducedList = []
    simplify(listpair, 0, len(listpair) - 1, tolerance, reducedList)
    reducedList.append(listpair[-1])
    return reducedList


def simplify(listpair, fromIndex, toIndex, tolerance, reducedList):
    dmax = 0
    index = 0
    for i in range(fromIndex + 1, toIndex):
        d = perpendicular_Distance(listpair[i], listpair[fromIndex], listpair[toIndex])
        if d > dmax:
            index = i
            dmax = d
    if dmax > tolerance:
        simplify(listpair, fromIndex, index, tolerance, reducedList)
        simplify(listpair, index, toIndex, tolerance, reducedList)
    else:
        reducedList.append(listpair[fromIndex])


def perpendicular_Distance(p, p1, p2):
    pOnLine = intercept(p, p1, p2)
    p_x = p[0]
    p_y = p[1]
    pl_x = pOnLine[0]
    pl_y = pOnLine[1]
    dx = pl_x - p_x
    dy = pl_y - p_y
    dist = math.sqrt(dx * dx + dy * dy) * 1000
    # dist = distance.distance(p, pOnLine)
    return dist


def intercept(p1, p2, p):
    p1_x = p1[0]
    p1_y = p1[1]
    p2_x = p2[0]
    p2_y = p2[1]
    p_x = p[0]
    p_y = p[1]

    if p1_x == p2_x:
        return [p1_x, p_y]
    elif p1_y == p2_y:
        return [p_x, p1_y]
    # y = mx + b for line p1p2
    p1p2_m = (p2_y - p1_y) / (p2_x - p1_x)
    p1p2_b = p1_y - p1p2_m * p1_x

    # y = mx + b for for line from point p to p1p2
    pp1p2_m = 0 - (1.0 / p1p2_m)
    pp1p2_b = p_y - pp1p2_m * p_x

    # find the point base on 'mx + b = mx + b'
    x_intersect = (p1p2_b - pp1p2_b) / (pp1p2_m - p1p2_m)
    y_intersect = p1p2_m * x_intersect + p1p2_b

    return [x_intersect, y_intersect]


# Function to do BR on list
# To group coordinates on the same street
def group_coor(list, groupList=[], apikey=''):
    # Version 2.0
    # Return a list of coordinate struct
    # coordinate = (lat, lon, address)
    # groupList = [[start coordinate, end coordinate], [start coor, ..., end coor], ...]

    # Get head, mid, tail point of list
    head = 0
    tail = len(list) - 1
    mid = (head + tail) // 2

    if tail >= head:

        # ===1: get the street name we are compairing with
        if len(groupList) != 0:
            # If the group list is not empty, means some coordinates are already in it
            # lastStreetName = " ".join(groupList[-1][-1].address.split(" ")[1:])
            lastStreetName = groupList[-1][-1].address
        else:
            # The group list is empty, nothing is in it
            lastStreetName = " ".join(reverse_Geocoding_streetNameOnly(list[0][0], list[0][1], apikey).split(" ")[1:])
            thisPair = Coordinate(list[0][0], list[0][1], lastStreetName)
            groupList.append([])
            groupList[0].append(thisPair)

        # ===2: get head, mid, and tail street names
        headStreetName = " ".join(reverse_Geocoding_streetNameOnly(list[head][0], list[head][1], apikey).split(" ")[1:])
        midStreetName = " ".join(reverse_Geocoding_streetNameOnly(list[mid][0], list[mid][1], apikey).split(" ")[1:])
        tailStreetName = " ".join(reverse_Geocoding_streetNameOnly(list[tail][0], list[tail][1], apikey).split(" ")[1:])

        # ===3
        # ------3.1
        if tailStreetName == lastStreetName:
            thisPair = Coordinate(list[tail][0], list[tail][1], tailStreetName)
            groupList[-1].append(thisPair)
            del list[:]
        # ------3.2
        elif headStreetName != lastStreetName:
            thisPair = Coordinate(list[head][0], list[head][1], headStreetName)
            groupList.append([])
            groupList[-1].append(thisPair)
            del list[0]
            groupList = group_coor(list, groupList, apikey)
        # ------3.3
        elif midStreetName == lastStreetName:
            thisPair = Coordinate(list[mid][0], list[mid][1], midStreetName)
            groupList[-1].append(thisPair)
            del list[:(mid + 1)]
            groupList = group_coor(list, groupList, apikey)
        # ------3.4
        else:
            groupList = group_coor(list[:mid], groupList, apikey)
            groupList = group_coor(list[mid:], groupList, apikey)

    return groupList


# Function to determine turning direction
def turning_direction(groupList):
    direction = ['Start']
    for index in range(len(groupList)-2):

        p1_lat, p1_lon = groupList[index][-2].lat, groupList[index][-2].lon
        p2_lat, p2_lon = groupList[index][-1].lat, groupList[index][-1].lon
        p3_lat, p3_lon = groupList[index + 1][0].lat, groupList[index + 1][0].lon
        p4_lat, p4_lon = groupList[index + 1][1].lat, groupList[index + 1][1].lon

        if p2_lat - p1_lat == 0:
            m1 = 0
        else:
            m1 = (p2_lon - p1_lon) / (p2_lat - p1_lat)
        if p4_lat - p3_lat == 0:
            m2 = 0
        else:
            m2 = (p4_lon - p3_lon) / (p4_lat - p3_lat)

        mForDeviation = (p3_lon - p1_lon) / (p3_lat - p1_lat)
        angle = round(math.atan((m2 - m1) / (1 + m2 * m1))) - 90
        if mForDeviation > 0:
            # positive slope for left to right
            if angle < 45:
                direction.append("Turn right")
            else:
                direction.append("Keep right")
        else:
            # negative slope for right to left,
            # case of horizontal and vertical will not exist
            if angle < 45:
                direction.append("Turn left")
            else:
                direction.append("Keep left")
    direction.append('End')
    return direction


def travel_distance(groupList):
    distanceList = [0]
    for group in groupList:
        dist = 0
        for each in range(len(group)-1):
            dist += (distance.distance((group[each].lat, group[each].lon), (group[each+1].lat, group[each+1].lon))).km
        dist = round(dist, 2)
        distanceList.append(dist)
    return distanceList


def main(argv):
    apikey = str(input("Enter your valid API key: "))
    list = read_GPX(argv)
    list = reduce_Coordinates(list,1)
    groupList = []
    group_coor(list, groupList, apikey)
    directionList = turning_direction(groupList)
    distanceList = travel_distance(groupList)

    newfile = xlsxwriter.Workbook("{0}.xlsx".format(argv[:-4]))
    worksheet = newfile.add_worksheet()
    row, col = 0, 0
    for index in range(len(groupList)):
        worksheet.write(row, col, directionList[index])
        worksheet.write(row, col+1, '{0}km'.format(distanceList[index]))
        worksheet.write(row, col+2, groupList[index][0].address)
        row += 1
    newfile.close()

    print("Finished!")


if __name__ == '__main__':
    main(sys.argv[1])


