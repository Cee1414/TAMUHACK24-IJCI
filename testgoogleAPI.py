import requests
import json


# f = open("airports.json", "w")
# response = requests.get("https://americanairlines-e02d72e53739.herokuapp.com/airports/all")
# if response.status_code == 200:
#     f.write(response.text)
# else:
#     print(response.status_code)

with open('airports.json', 'r') as file:
    data_array = json.load(file)



OriginsWithCoordinates = {}

for flight in data_array:
    flightName = flight['code']
    latitude = flight['location']['latitude']
    longitude = flight['location']['longitude']
    OriginsWithCoordinates[flightName] = [latitude, longitude]
    

print("All Coordinates:", OriginsWithCoordinates)

# response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?destinations=New%20York%20City%2C%20NY&origins=Washington%2C%20DC&units=imperial&key=AIzaSyDOEnQPZxu06yhdUz6Kv3OiUV3fHPCNPbY")
# if response.status_code == 200:
#     f.write(response.text)
# else:
#     print(response.status_code)