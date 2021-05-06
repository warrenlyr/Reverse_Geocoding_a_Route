import gpxpy
import requests
import math


# APIKey: 46aa2599e2e24695a67d516aea17b69a
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


def reduce_Coordinates(listpair, tolerance):
    dmax = 0
    index = 0
    end = len(listpair)-1
    for i in range(0, end):
        d = perpendicular_Distance(listpair[i], listpair[0], listpair[end])
        if d > dmax:
            index = i
            dmax = d

    resultList = []

    if dmax > tolerance:
        recResult1 = reduce_Coordinates(listpair[0, index], tolerance)
        recResult2 = reduce_Coordinates(listpair[index, end], tolerance)

        resultList = [recResult1[0, len(recResult1) - 1], recResult2[0, len(recResult2)]]
    else:
        resultList = [listpair[0], listpair[end]]

    return resultList


def perpendicular_Distance(p, p1, p2):
    pOnLine = intercept(p, p1, p2)
    p_x = p[0]
    p_y = p[1]
    pl_x = pOnLine[0]
    pl_y = pOnLine[1]
    dx = pl_x - p_x
    dy = pl_y - p_y
    return math.sqrt(dx * dx + dy * dy)


def intercept(p1, p2, p):
    p1_x = p1[0]
    p1_y = p1[1]
    p2_x = p2[0]
    p2_y = p2[1]
    p_x = p[0]
    p_y = p[1]

    if p1_x == p2_x:
        return p1_x, p_y
    elif p1_y == p2_y:
        return p_x, p1_y
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


def reverse_Geocoding(latitude, longitude):
    info = {'apiKey': '46aa2599e2e24695a67d516aea17b69a', 'version': 4.10, 'lat': latitude, 'lon': longitude}
    response = requests.get(
        'https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP/default.aspx', params=info)
    string = response.content.decode('utf-8')
    list = string.split(',')
    address = "{0} {1} {2} {3}".format(list[5], list[6], list[7], list[8])
    return address


if __name__ == '__main__':
    list = read_GPX('test.gpx')
    # for pair in list:
    #     print("{0},{1}".format(str(pair[0]), str(pair[1])))
    #     print(reverse_Geocoding(pair[0], pair[1]))
    #     print('\n')
    # print("Before reducing!!!!!!!!!!!!!!!!!!!!!")
    list = reduce_Coordinates(list, 0.01)
    for pair in list:
        print("{0},{1}".format(str(pair[0]), str(pair[1])))
        print(reverse_Geocoding(pair[0], pair[1]))
        print('\n')

