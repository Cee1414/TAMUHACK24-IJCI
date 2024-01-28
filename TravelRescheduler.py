import requests
import json
import numpy as np

# f = open("airports.json", "w")
# response = requests.get("https://americanairlines-e02d72e53739.herokuapp.com/airports/all")
# if response.status_code == 200:
#     f.write(response.text)
# else:
#     print(response.status_code)
# f.close()

# f = open("airports.json", "r")
# airports = json.load(f)
# f.close()

# originsWithCoordinates = {}

# for airport in airports:
#     airportName = airport['code']
#     latitude = airport['location']['latitude']
#     longitude = airport['location']['longitude']
#     originsWithCoordinates[airportName] = [latitude, longitude]
    

# print("All Coordinates:", originsWithCoordinates)

# f = open("/mnt/c/Users/camso/CSCE221/googleAPIkey.txt", "r")
# key = f.read().strip()

# slice1 = "https://maps.googleapis.com/maps/api/distancematrix/json?destinations="
# slice2 = "&origins="
# slice3 = f'&key={key}'

# for originKey in originsWithCoordinates:
#     originCoords = f'{originsWithCoordinates[originKey][0]}%2C{originsWithCoordinates[originKey][1]}'
#     distanceForOrigin = {}
#     # originCoords = urllib.parse.quote_plus(originCoords)
#     for destinationKey in originsWithCoordinates:
#     # for i in range(1):
#         destinationCoords = f'{originsWithCoordinates[destinationKey][0]}%2C{originsWithCoordinates[destinationKey][1]}'
#         # destinationCoords = urllib.parse.quote_plus(destinationCoords)
#         response = requests.get(slice1+destinationCoords+slice2+originCoords+slice3)
#         # print(slice1+destinationCoords+slice2+originCoords+slice3)
#         f = open("originToDest.json", "w")
#         if response.status_code == 200:
#             f.write(response.text)
#         else:
#             print(response.status_code)
#         f.close()

#         f = open("originToDest.json", "r")
#         drivedata = json.load(f)
#         f.close()
#         # for data in drivedata:
#         time = drivedata['rows'][0]['elements'][0]['duration']['value']
#         distanceForOrigin[destinationKey] = time
#     keys = list(distanceForOrigin.keys())
#     values = list(distanceForOrigin.values())
#     sorted_value_index = np.argsort(values)
#     sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
 
#     print(sorted_dict)

def getOriginDictionary(originKey):
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
    f = open("/mnt/c/Users/camso/CSCE221/googleAPIkey.txt", "r")
    key = f.read().strip()
    slice1 = "https://maps.googleapis.com/maps/api/distancematrix/json?destinations="
    slice2 = "&origins="
    slice3 = f'&key={key}'
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
        time = round(drivedata['rows'][0]['elements'][0]['duration']['value']/60)
        distanceForOrigin[destinationKey] = time
    keys = list(distanceForOrigin.keys())
    values = list(distanceForOrigin.values())
    sorted_value_index = np.argsort(values)
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
    return sorted_dict

def convertStringToFloat(timeString):
    hours, minutes = map(int, timeString.split(':'))
    total_minutes = hours * 60 + minutes
    time_float = float(total_minutes)
    return time_float

def possibleConnection(origin, dest, date, time):
    response = requests.get(f"https://americanairlines-e02d72e53739.herokuapp.com/flights?date={date}&origin={origin}&destination={dest}")
    f = open("flightData.json", "w")
    if response.status_code == 200: 
        f.write(response.text)
    f.close()
    
    f = open("flightData.json", "r")
    flightData = json.load(f)
    f.close()

    for flight in flightData:
        if convertStringToFloat((flight['departureTime'])[-4:])>time:
            return flight
        
    return False
        

def main():
    #known variables
    flightnumber = "9722"
    date = "2020-01-01"
    origin = "DFW"
    finalDest = "GSO"
    originalDeparture = "00:00"
    flight = "NA"
    destDict = getOriginDictionary(origin)
    driveTime = 0
    driveDest = "Null"
    for dest in destDict:
        if dest == origin:
            continue
        time = convertStringToFloat(originalDeparture) + destDict[dest]
        if possibleConnection(dest, finalDest, date, time) == False:
           continue
        else:
            flight = possibleConnection(dest, finalDest, date, time)
            driveTime = time
            driveDest = dest
            break
    # print(flight)
    print(f"Flight {flightnumber} from {origin} to {finalDest} was cancelled. No other flight at DFW is available for the remainder of the day.")
    print(f"We have created a travel plan for you to make it to you destination by the end of the day and is as follows.")
    print(f"Complementary rental car from {origin} to {driveDest} taking {driveTime} minutes.")
    print(f"You are rescheduled to flight {flight['flightNumber']} from {driveDest} to {finalDest} departing at {(flight['departureTime'])[-4:]} and arriving at {(flight['arrivalTime'])[-4:]}.")



if __name__ == "__main__":
    main()



        








# response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?destinations=New%20York%20City%2C%20NY&origins=Washington%2C%20DC&units=imperial&key=AIzaSyDOEnQPZxu06yhdUz6Kv3OiUV3fHPCNPbY")
# if response.status_code == 200:
#     f.write(response.text)
# else:
#     print(response.status_code)