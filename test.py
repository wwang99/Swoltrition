import requests
import json

food = 'brownies'
search_payload = {'format': 'json', 'q': food, 'ds': 'Standard Reference', 'max': '1', 'api_key': 'AY1U6UdBQKwgOcvSaQVhLqcu5QdHagIPWgAQvHtU'}
search_request = requests.get('http://api.nal.usda.gov/ndb/search/?', params = search_payload)
print search_request.url
searchresults = json.loads(search_request.text)
foodid = searchresults['list']['item'][0]["ndbno"]
nutrients_payload = {'ndbno': foodid, 'type': 'b', 'format': 'json', 'api_key': 'AY1U6UdBQKwgOcvSaQVhLqcu5QdHagIPWgAQvHtU'}
nutrients_request = requests.get('http://api.nal.usda.gov/ndb/reports/?', params = nutrients_payload)
print nutrients_request.url

fooddata=json.loads(nutrients_request.text)
foodname = fooddata['report']['food']["name"]
protein = fooddata['report']['food']['nutrients'][2]["value"]
fat = fooddata['report']['food']['nutrients'][3]["value"]
carbs = fooddata['report']['food']['nutrients'][4]["value"]