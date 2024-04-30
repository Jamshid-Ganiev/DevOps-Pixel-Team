import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
loc1 = "Washington, D.C."
loc2 = "Baltimore, Maryland"
key = "a68dd598-77c7-4886-9da1-425720c4092e"

def geocoding (location, key):
    while location == "":
        location = input("Enter the location again: ") 
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1","key":key})
    
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    # print("Geocoding API URL for " + location + ":\n" + url)
    
    if json_status == 200 and len(json_data["hits"]) !=0:
        json_data = requests.get(url).json()
        lat=(json_data["hits"][0]["point"]["lat"])
        lng=(json_data["hits"][0]["point"]["lng"])
    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status != 200: 
            print("Geocode API status: " + str(json_status) + "\nError message: " + 
            json_data["message"]) 
    return json_status,lat,lng 


while True:
    loc1 = input("Starting Location: ")
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)
    print(orig)
    
    loc2 = input("Destination: ")
    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)
    print(dest)  