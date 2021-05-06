'''
Project 1 part 2:
Do BR on requested coordinates first,
then get the start point and end point for each street
# APIKey: 46aa2599e2e24695a67d516aea17b69a
'''
'''
Update 10/10/2020
Using read_GPX and reverse_Geocoding function from part, wrote by John
update BR search on coordinates
==========
Update 10/18/2020
Return coordinates struct now
a list of coordinate struct 
list = [[start coor, ..., end coor], ...]
coor = (lat, lon, address)
'''

import gpxpy
import requests
import os

class Coordinate:
    def __init__(self, lat, lon, add):
        self.lat = lat
        self.lon = lon
        self.address = add

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
    #list = [[long, lat], [x, y], ...]

def reverse_Geocoding(latitude, longitude):
    info = {'apiKey': '46aa2599e2e24695a67d516aea17b69a', 'version': 4.10, 'lat': latitude, 'lon': longitude}
    response = requests.get(
        'https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP/default.aspx', params=info)
    string = response.content.decode('utf-8')
    list = string.split(',')
    address = "{0} {1} {2} {3}".format(list[5], list[6], list[7], list[8])
    return address

def reverse_Geocoding_streetNameOnly(latitude, longitude):
    info = {'apiKey': '46aa2599e2e24695a67d516aea17b69a', 'version': 4.10, 'lat': latitude, 'lon': longitude}
    response = requests.get(
        'https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP/default.aspx', params=info)
    string = response.content.decode('utf-8')
    list = string.split(',')
    address = "{0}".format(list[5])
    return address

def group_coor(list, groupList = []):
    ### OLD ###
    #GroupList = [[[street name, headStartPoint, headEndPoint],[street name, tailStartPoint, tailEndPoint]], ...]
    ### NEW ###
    #GroupList = [[start coor, end coor], [start coor, ...., end coor], ...]
    '''
    Now return a list of Corrdinate
    '''
    head = 0
    tail = len(list) - 1
    mid = 0


    #Get last street name
    #If the groupList is not empty, the street name in the last index is what we are finding right now
    if len(groupList) != 0:
        #lastStreetName = " ".join(groupList[-1][-1][0].split(" ")[1:])
        lastStreetName = " ".join(groupList[-1][-1].address.split(" ")[1:])
    #Otherwise, the groupList is empty, we add one to it
    #And add street name, long, lat to the groupList[0]
    else:
        lastStreetName = " ".join(reverse_Geocoding_streetNameOnly(list[0][0], list[0][1]).split(" ")[1:])
        #thisPair = [reverse_Geocoding_streetNameOnly(list[0][0], list[0][1]), list[0][0], list[0][1]]
        thisPair = Coordinate(list[0][0], list[0][1], reverse_Geocoding_streetNameOnly(list[0][0], list[0][1]))
        groupList.append([])
        groupList[0].append(thisPair)

    #Begin here
    #If >= 1 coordinate(s) is/are remaining
    if tail >= head:
        #Get mid point and all streets names of head, mid, tail points
        mid = (head + tail) // 2
        headStreetName = " ".join(reverse_Geocoding_streetNameOnly(list[head][0], list[head][1]).split(" ")[1:])
        midStreetName = " ".join(reverse_Geocoding_streetNameOnly(list[mid][0], list[mid][1]).split(" ")[1:])
        tailStreetName = " ".join(reverse_Geocoding_streetNameOnly(list[tail][0], list[tail][1]).split(" ")[1:])

        #First check if the tail street name
        if tailStreetName == lastStreetName:
            #thisPair = [reverse_Geocoding_streetNameOnly(list[tail][0], list[tail][1]), list[tail][0], list[tail][1]]
            thisPair = Coordinate(list[tail][0], list[tail][1], reverse_Geocoding_streetNameOnly(list[tail][0], list[tail][1]))
            groupList[-1].append(thisPair)
            del list[:]

        #Second if the head street name is diff with the street name we are looking for now
        elif headStreetName != lastStreetName:
            #thisPair = [reverse_Geocoding_streetNameOnly(list[head][0], list[head][1]), list[head][0], list[head][1]]
            thisPair = Coordinate(list[head][0], list[head][1], reverse_Geocoding_streetNameOnly(list[head][0], list[head][1]))
            groupList.append(thisPair)
            del list[0]
            groupList = group_coor(list, groupList)

        #Third if mid point street name is diff with the street name we are looking for now
        elif midStreetName == lastStreetName:
            #thisPair = [reverse_Geocoding_streetNameOnly(list[mid][0], list[mid][1]), list[mid][0], list[mid][1]]
            thisPair = Coordinate(list[mid][0], list[mid][1], reverse_Geocoding_streetNameOnly(list[mid][0], list[mid][1]))
            groupList[-1].append(thisPair)
            del list[:(mid + 1)]
            groupList = group_coor(list, groupList)

        #Otherwise, do the same algorithm on the first and second part of exsiting coordinates list we have
        else:
            listFirstHalf = list[:mid]
            listSecondHalf = list[mid:]
            groupList = group_coor(listFirstHalf, groupList)
            groupList = group_coor(listSecondHalf, groupList)

    #When it's done, return the grouped coordinates list
    else:
        return groupList    
'''
def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()
'''


if __name__ == '__main__':
    '''
    list = read_GPX('test.gpx')
    print("first add: ", reverse_Geocoding_streetNameOnly(list[0][0], list[0][1]))
    print("length: ", len(list))
    print("Now print list: ")
    print(list)
    
    a = input("xxx: ")
    if(a):
        print("success")
    else:
        print("no")
    
    print(string_similar('922 NW Circle Blvd', '134567 NW Circle Blvd'))
    a = " ".join(('922 NW Circle Blvd').split(" ")[1:])
    print(a)
    
    list = [[["11th ave", 123, 456], ["11th ave", 321, 654]], [["12th ave", 123, 456], ["12th ave", 321, 654]]]
    print(list[-1][-1][0], list[-1][-1][1],list[-1][-1][2])
    '''
    
    list = read_GPX('test.gpx')
    groupList = []
    group_coor(list, groupList)
    print("Now list is: ", list)
    print("Now group list is: ")
    for group in groupList:
        for coor in group:
            print("coor: ", coor.lat, coor.lon, coor.address)
    
    '''
    print("Group list[0]: ", groupList[0], "\n")
    print(groupList[0][0][0], "\n")
    print(groupList[0][1], "\n")
    '''
    '''
    [['922 NW Circle Blvd', 44.587662, -123.256691, ['966 NW Circle Blvd', 44.5875429, -123.258827]]]
    [[['922 NW Circle Blvd', 44.587662, -123.256691]]]
    '''