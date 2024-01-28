import requests
import json
import numpy as np

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

f = open("/mnt/c/Users/camso/CSCE221/googleAPIkey.txt", "r")
key = f.read().strip()

slice1 = "https://maps.googleapis.com/maps/api/distancematrix/json?destinations="
slice2 = "&origins="
slice3 = f'&key={key}'

for originKey in originsWithCoordinates:
    originCoords = f'{originsWithCoordinates[originKey][0]}%2C{originsWithCoordinates[originKey][1]}'
    distanceForOrigin = {}
    # originCoords = urllib.parse.quote_plus(originCoords)
    for destinationKey in originsWithCoordinates:
    # for i in range(1):
        destinationCoords = f'{originsWithCoordinates[destinationKey][0]}%2C{originsWithCoordinates[destinationKey][1]}'
        # destinationCoords = urllib.parse.quote_plus(destinationCoords)
        response = requests.get(slice1+destinationCoords+slice2+originCoords+slice3)
        # print(slice1+destinationCoords+slice2+originCoords+slice3)
        f = open("originToDest.json", "w")
        if response.status_code == 200:
            f.write(response.text)
        else:
            print(response.status_code)
        f.close()

        f = open("originToDest.json", "r")
        drivedata = json.load(f)
        f.close()
        # for data in drivedata:
        time = drivedata['rows'][0]['elements'][0]['duration']['value']
        distanceForOrigin[destinationKey] = time
    keys = list(distanceForOrigin.keys())
    values = list(distanceForOrigin.values())
    sorted_value_index = np.argsort(values)
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
 
    print(sorted_dict)



        








# response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?destinations=New%20York%20City%2C%20NY&origins=Washington%2C%20DC&units=imperial&key=AIzaSyDOEnQPZxu06yhdUz6Kv3OiUV3fHPCNPbY")
# if response.status_code == 200:
#     f.write(response.text)
# else:
#     print(response.status_code)