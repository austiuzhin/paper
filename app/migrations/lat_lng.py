from d_base import Item
from d_base import db_session
import requests
import json
import sys
import re
from app.migrations.d_base import Item
from sqlalchemy.sql.expression import func
#import googlemaps

def yandex_geocode(request):
    # with open('static/map_api_key.txt','r') as file:
    #       api_key = file.readline()

    # total = Item.query.filter(Item.id).count()
    # total_n = Item.query.filter(Item.lat == None).count()

    # gmaps = googlemaps.Client(key=api_key)
    # geocode_result = gmaps.geocode(address_string)
    # lat = geocode_result[0].get('geometry').get('location').get('lat')
    # lng = geocode_result[0].get('geometry').get('location').get('lng')


    #this was for sys.argv testing ### request = ''.join(request[1:])
    request = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?№]', request.lower())
    request = (' '.join(request)).replace(' ','')
    #print (request)
    
    data = requests.get('https://geocode-maps.yandex.ru/1.x/?geocode={}&format=json&results=1'.format(request))
    
    query_result = json.loads(data.text)
    response_result = query_result.get('response').get('GeoObjectCollection').get('metaDataProperty').get('GeocoderResponseMetaData').get('found')
    if int(response_result) > 0:
        lat_lng_string = query_result.get('response').get('GeoObjectCollection').get('featureMember')[0] \
                        .get('GeoObject').get('Point').get('pos')
        lat_lng_list = [float(item) for item in lat_lng_string.split(' ')]
        #print (response_result)
        return lat_lng_list[1], lat_lng_list[0]
    else:
        return None, None

def adding_coords(counter = None):
    print ('Добавляю координаты...')
    if not counter:
        counter = db_session.query(Item).filter(func.length(Item.obj_address) >= 20) \
        .filter(Item.lat == None).count()
    
    objects_without_coords_id=[x.id for x in db_session.query(Item) \
     .filter(func.length(Item.obj_address) >= 20).filter(Item.lat == None) \
     .distinct()]
    
    for instance in objects_without_coords_id: 
        if counter == 0:
            break
        else:
            item = db_session.query(Item).get(instance)
            address = item.obj_address
            lat, lng = yandex_geocode(address)
            item.lat = lat
            item.lng = lng
            #print (item.id, item.obj_address,item.lat, item.lng)            
            counter -= 1
    print ('Координаты добавлены.')
    db_session.commit()

def main(argv):
    if len(argv) == 1:
        adding_coords()
    else: 
        adding_coords(int(argv[1]))
    
if __name__ == '__main__':
    main(sys.argv)

