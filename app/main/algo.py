import googlemaps
#from paar.app.server import db
from app.migrations.d_base import Item, db_session
import numpy as np
from scipy.spatial import distance

def get_key_for_sorting(item):
    return item[1]

def top_five_distances(input_type, input_room, input_address):

    with open('./static/map_api_key.txt','r') as file:
        api_key = file.readline()
    
    gmaps = googlemaps.Client(key=api_key)
    geocode_result = gmaps.geocode(input_address)
    
    # here i need if statment with
    #   returned answer from Google
    #
    spot_lat = geocode_result[0].get('geometry').get('location').get('lat')
    spot_lng = geocode_result[0].get('geometry').get('location').get('lng')
    spot_np_array = np.array([spot_lat,spot_lng])
    
    if input_room == 5:
        objects_wth_coords_lst = db_session.query(Item).filter(Item.lat != None).filter(Item.lng !=None)\
        .filter(Item.obj_type == input_type).filter(Item.rooms >= input_room).all()
    else:
        objects_wth_coords_lst = db_session.query(Item). \
         filter(Item.lat != None).filter(Item.lng !=None) \
         .filter(Item.obj_type == input_type).filter(Item.rooms == input_room).all()

    nearest_spots_list = list()

    for instance in objects_wth_coords_lst:
        
        instance_lat = db_session.query(Item).get(instance.id).lat
        instance_lng = db_session.query(Item).get(instance.id).lng
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
    with open('./static/map_api_key.txt','r') as file:
        api_key = file.readline()   
    gmaps = googlemaps.Client(key=api_key)
    ins_id, distance_text, duration_text, duration_value = list(),list(),list(),list()
    for instance_id in nearest_spots_ids_list:
        instance_lat = db_session.query(Item).get(instance_id).lat
        instance_lng = db_session.query(Item).get(instance_id).lng
        instance_lat_lng_tuple = tuple((instance_lat,instance_lng))
        way = gmaps.distance_matrix(instance_lat_lng_tuple,spot_coords,mode = "walking",language = "ru", units = "metric")
        if way.get('rows')[0].get('elements')[0].get('status') == 'OK':
            #ins_id.append(Item.query.get(instance_id).name)
            ins_id.append(instance_id)
            distance_text.append(way.get('rows')[0].get('elements')[0].get('distance').get('text'))
            duration_text.append(way.get('rows')[0].get('elements')[0].get('duration').get('text'))
            duration_value.append(way.get('rows')[0].get('elements')[0].get('duration').get('value'))           
        else:
            ins_id.append(None)
            distance_text.append(None)
            duration_text.append(None)
            duration_value.append(None) 
    return ins_id, distance_text, duration_text, duration_value


# def main():
#     nearest_spots_ids, spot_coord = top_five_distances(argv)
#     ins_id, distance_text, duration_text, duration_value = distance_matrix_walk(nearest_spots_ids, spot_coord)
#     for item in range(len(ins_id)):
#         print ("Объект {}. \n\n Расстояние пешком: {}, приблизительное время ходьбы {}".format(name[item],distance_text[item], duration_text[item]))

if __name__ == '__main__':
    #(timeit.Timer(top_five_distances('Москва, Расковой 32'))).timeit(number=1)
    main()