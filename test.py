import requests
import json

search_query = 'brownies'
search_payload = {'format': 'json', 'api_key': 'AY1U6UdBQKwgOcvSaQVhLqcu5QdHagIPWgAQvHtU', 'q': search_query, 'ds': 'Standard Reference', 'max': '1'}
search_request = requests.get('http://api.nal.usda.gov/ndb/search/?', params = search_payload)
print search_request.url

searchresults=json.loads(search_request.text)
print searchresults['list']['item'][0]["ndbno"]
foodid = searchresults['list']['item'][0]["ndbno"]

nutrients_payload = {'ndbno': foodid, 'type': 'b', 'format': 'json', 'api_key': 'AY1U6UdBQKwgOcvSaQVhLqcu5QdHagIPWgAQvHtU'}
nutrients_request = requests.get('http://api.nal.usda.gov/ndb/reports/?', params = nutrients_payload)
print nutrients_request.url

fooddata=json.loads(nutrients_request.text)
print fooddata['report']['food']['nutrients'][2]["value"] + ' g protein'
protein = fooddata['report']['food']['nutrients'][2]["value"]
print protein
print fooddata['report']['food']['nutrients'][3]["value"] + ' g fats'
print fooddata['report']['food']['nutrients'][4]["value"] + ' g carbs'