from d_base import Item
import googlemaps


with open('static/map_api_key.txt','r') as file:
		api_key = file.readline()

total = Item.query.filter(Item.id).count()
total_n = Item.query.filter(Item.lat == None).count()

gmaps = googlemaps.Client(key=api_key)
geocode_result = gmaps.geocode(address_string)
lat = geocode_result[0].get('geometry').get('location').get('lat')
lng = geocode_result[0].get('geometry').get('location').get('lng')