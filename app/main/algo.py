import sys
import googlemaps
from app.server import db
from app.migrations.d_base import Item
import numpy as np
from scipy.spatial import distance

def get_key_for_sorting(item):
	return item[1]

def top_five_distances(argv):

	with open('../static/map_api_key.txt','r') as file:
		api_key = file.readline()
	
	gmaps = googlemaps.Client(key=api_key)
	geocode_result = gmaps.geocode(argv)
	
	# here i need if statment with
	#	returned answer from Google
	#
	spot_lat = geocode_result[0].get('geometry').get('location').get('lat')
	spot_lng = geocode_result[0].get('geometry').get('location').get('lng')
	spot_np_array = np.array([spot_lat,spot_lng])

	objects_wth_coords_lst = test_lst = db.session.query(Item)\
	.filter(Item.lat != None).filter(Item.lng !=None).all()

	nearest_spots_list = list()

	for instance in objects_wth_coords_lst:
		
		instance_lat = db.session.query(Item).get(instance.id).lat
		instance_lng = db.session.query(Item).get(instance.id).lng
		instance_np_array = np.array([instance_lat,instance_lng])
		dist_btw_spots = distance.cosine(spot_np_array,instance_np_array)
		if not nearest_spots_list:
			nearest_spots_list.append([instance.id,dist_btw_spots])
		else:
			already_added_distances = [nearest_spots_list[item][1] for item in range(len(nearest_spots_list))]
			if all(dist >= dist_btw_spots for dist in already_added_distances):
				continue
			else:
				nearest_spots_list.append([instance.id,dist_btw_spots])
	sorted_nearest_spots = sorted(nearest_spots_list, key = get_key_for_sorting)
	finding_nearest_spots_id = sorted_nearest_spots[:5]
	nearest_spots_ids = [finding_nearest_spots_id[item][0] for item in range(len(finding_nearest_spots_id))]
	#print ((timeit.Timer(lambda: top_five_distances('Москва, Расковой 32'))).timeit(number=1))
	#время обработки одного запроса алгоритма 211.83238828929416 сек ~ 3 мин 32 сек.
	return nearest_spots_ids, tuple((spot_lat, spot_lng))


def distance_matrix_walk(nearest_spots_ids_list, spot_coords):
	with open('../static/map_api_key.txt','r') as file:
		api_key = file.readline()	
	gmaps = googlemaps.Client(key=api_key)
	name, distance_text, duration_text, duration_value = list(),list(),list(),list()
	for instance_id in nearest_spots_ids_list:
		instance_lat = db.session.query(Item).get(instance_id).lat
		instance_lng = db.session.query(Item).get(instance_id).lng
		instance_lat_lng_tuple = tuple((instance_lat,instance_lng))
		way = gmaps.distance_matrix(instance_lat_lng_tuple,spot_coords,mode = "walking",language = "ru", units = "metric")
		if way.get('rows')[0].get('elements')[0].get('status') == 'OK':
			name.append(db.session.query(Item).get(instance_id).name)
			distance_text.append(way.get('rows')[0].get('elements')[0].get('distance').get('text'))
			duration_text.append(way.get('rows')[0].get('elements')[0].get('duration').get('text'))
			duration_value.append(way.get('rows')[0].get('elements')[0].get('duration').get('value'))			
		else:
			name.append("Не пришёл ответ от сервера по построению пути Google.")
			distance_text.append("Не пришёл ответ от сервера по построению пути Google.")
			duration_text.append("Не пришёл ответ от сервера по построению пути Google.")
			duration_value.append(None)	
	return name, distance_text, duration_text, duration_value


def main(argv):
	nearest_spots_ids, spot_coord = top_five_distances(argv)
	name, distance_text, duration_text, duration_value = distance_matrix_walk(nearest_spots_ids, spot_coord)
	for item in range(len(name)):
		print ("Объект {}. \n\n Расстояние пешком: {}, приблизительное время ходьбы {}".format(name[item],distance_text[item], duration_text[item]))

if __name__ == '__main__':
	#(timeit.Timer(top_five_distances('Москва, Расковой 32'))).timeit(number=1)
	main(sys.argv)