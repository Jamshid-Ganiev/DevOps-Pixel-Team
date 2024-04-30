import requests 
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?" 
route_url = "https://graphhopper.com/api/1/route?" 
loc1 = "Rome, Italy" 
loc2 = "Baltimore, Maryland" 
key = "a68dd598-77c7-4886-9da1-425720c4092e" # Replace with your Graphhopper API key

url = geocode_url + urllib.parse.urlencode({"q":loc1, "limit": "1", "key":key})

replydata = requests.get(url) 
json_data = replydata.json() 
json_status = replydata.status_code 
print(json_data)

