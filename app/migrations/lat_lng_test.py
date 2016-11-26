from d_base import Item, db_session
import requests
import json
import re
from app.migrations.d_base import Item
from sqlalchemy.sql.expression import func

def yandex_geocode(request):
    request = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?№]', request.lower())
    request = (' '.join(request)).replace(' ','')
    
    data = requests.get('https://geocode-maps.yandex.ru/1.x/?geocode={}&format=json&results=1'.format(request))
    
    query_result = json.loads(data.text)
    response_result = query_result.get('response').get('GeoObjectCollection').get('metaDataProperty').get('GeocoderResponseMetaData').get('found')
    if int(response_result) > 0:
        lat_lng_string = query_result.get('response').get('GeoObjectCollection').get('featureMember')[0] \
                        .get('GeoObject').get('Point').get('pos')
        lat_lng_list = [float(item) for item in lat_lng_string.split(' ')]
        return lat_lng_list[1], lat_lng_list[0]
    else:
        return None, None

def adding_coords(counter):
    print ('Добавляю координаты...')
    if not counter:
        counter = int(argv[1])
    objects_without_coords_id=[x.id for x in Item.query.filter(func.length(Item.obj_address) >= 20).filter(Item.lat == None).filter(Item.lng == None).distinct()]    
    db_session.close()
    for instance in objects_without_coords_id: 
        db_session.commit()
        if counter == 0:
            break
        else:
            another_item = Item.query.get(instance)
            address = another_item.obj_address
            lat, lng = yandex_geocode(address)
            another_item.lat = lat
            another_item.lng = lng
            print (another_item.id, another_item.obj_address,another_item.lat, another_item.lng)
            counter -= 1
    db_session.commit()
    print ('Координаты добавлены.')

def main():
    adding_coords()
    db_session.commit()

if __name__ == '__main__':
    main()

