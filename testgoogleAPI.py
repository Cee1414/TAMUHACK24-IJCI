import requests
import json
import urllib.parse


f = open("airports.json", "w")
response = requests.get("https://americanairlines-e02d72e53739.herokuapp.com/airports/all")
if response.status_code == 200:
    f.write(response.text)
else:
    print(response.status_code)
f.close()

f = open("airports.json", "r")
airports = json.load(f)
f.close()

originsWithCoordinates = {}

for airport in airports:
    airportName = airport['code']
    latitude = airport['location']['latitude']
    longitude = airport['location']['longitude']
    originsWithCoordinates[airportName] = [latitude, longitude]
    

print("All Coordinates:", originsWithCoordinates)

slice1 = "https://maps.googleapis.com/maps/api/distancematrix/json?destinations="
slice2 = "&origins="
slice3 = "&key=/mnt/c/Users/camso/CSCE221/googleAPIkey.txt"

for originKey in originsWithCoordinates:
    originCoords = f'{originsWithCoordinates[originKey][0]} {originsWithCoordinates[originKey][1]}'
    
    for destinationKey in originsWithCoordinates:
        destinationCoords = f'{originsWithCoordinates[destinationKey][0]} {originsWithCoordinates[destinationKey][1]}'




# response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?destinations=New%20York%20City%2C%20NY&origins=Washington%2C%20DC&units=imperial&key=AIzaSyDOEnQPZxu06yhdUz6Kv3OiUV3fHPCNPbY")
# if response.status_code == 200:
#     f.write(response.text)
# else:
#     print(response.status_code)