import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "6b2435ab-f952-4fed-9754-a61d9bfff722"

def geocoding(location):
    while location == "":
        location = input("Enter the location again: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
    else:
        lat = "null"
        lng = "null"
        if json_status != 200:
            print("Geocode API status: " + str(json_status) + "\nError message: " +
                  json_data["message"])
    return json_status, lat, lng


while True:
    loc1 = input("Starting Location: ")
    if loc1.lower() == "quit" or loc1.lower() == "q":
        break
    orig = geocoding(loc1)
    loc2 = input("Destination: ")
    if loc2.lower() == "quit" or loc2.lower() == "q":
        break
    dest = geocoding(loc2)
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()

        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" +
              paths_url)

        if paths_status == 200:
            distance = paths_data.get("paths")[0].get("distance")
            time = paths_data.get("paths")[0].get("time")

            result = {
                "API status": "Success",
                "Distance to the destination": distance,
                "Time traveled (seconds)": time,
                "Longitude": [orig[2], dest[2]],
                "Latitude": [orig[1], dest[1]]
            }

            print("Result:")
            print(json.dumps(result, indent=4))
        else:
            print("Routing API Status: " + str(paths_status))
    else:
        print("Error occurred while geocoding. Please try again.")

