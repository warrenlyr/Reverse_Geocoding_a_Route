import gpxpy
import requests


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
    for pair in list:
            print("{0},{1}".format(str(pair[0]), str(pair[1])))
            print(reverse_Geocoding(pair[0], pair[1]))
            print('\n')
