# README #

Update 10/23/2020

## Project Info ##
* University of Oregon Fall 2020 CIS 422 Group Project 1
* This project is to convert coordinates from user’s inputs into navigating information including road name, travel distance, and turning direction. The input should include manual input and .gpx file input, and the user interface should be a webpage that allows users to enter or drag files to upload. But because of something that happened during the project, our program only performs a command-line UI and only allows .gpx file as standard input.
* Project details: https://uo-cis422.github.io/chapters/projects/reverse/reverse.html
* Member: Yiran Liu, John Zhou

## Packages ##
* gpxpy
* requests
* math
* sys
* xlsxwriter
* geopy
```
To install these packages if you don't have, use the command:
pip install "<package name>"
```
 
## How to run ##
```
python3 main.py <.gpx file name>
```

## Building Process ##
### Begining ##
#### We have sperated the project to 4 parts ####
* Part 1: Data extracting and size reducing --- John
* Part 2: API and Binary Reasearching to group coordinates on the same street --- Yiran
* Part 3: Determine turning direction and travel distance --- John
* part 4: Document, organize, and managment --- Yiran
### Part 1 ###
* In this part, the program will read all the coordinates from the gpx file, and store them as a 2D list. After that, it will gernerate the algrithom called Ramer-Douglas-Peucker, to reduce the size of list through deleting unnessary coordinates. 
* More information about this algrithom: https://en.wikipedia.org/wiki/Ramer–Douglas–Peucker_algorithm
### Part 2 ###
* In this part, the progarm will do the binary searching to the 2D list from part1, and create a 2D list contains the starting and ending points of each street with its street name and coordinates by the address of each coordinate from API. 
* More information about API: https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP.aspx
### Part 3 ###
* In this part, the program will find the turning points and its turning direction and travel distance to this point.
### Part 4 ###
* Organized the files
* Reorganized Bitbucket to make it more clear
* Complete ReadMe and project report
