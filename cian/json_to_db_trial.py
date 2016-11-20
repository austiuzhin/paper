from create_db import db_session, Flat, Price
import json
import codecs
from datetime import datetime
from geopy.geocoders import Yandex


def out_of_file(filename):
	with codecs.open(filename,'r','cp1251') as f_opened:
		return json.load(f_opened)


def write_to_db_one(data_list,start_number):
	counter = start_number
	for item in data_list:
		if counter <= (start_number - 1 + 25000):
			try:
				db_session.query(Flat.href).filter(Flat.href==item["href"]).first()[0]
			except TypeError:
				item_type = item["type"]
				date = item["date"]
				metro_station = item["metro_station"]
				object_address = item["obj_address"]
				rooms = item["rooms"]
				area = item["area"]
				floor = item["floor"]
				href = item["href"]
				source = item["source"]
				name = item["name"]
				try:
					geolocator = Yandex()
					location = geolocator.geocode(object_address)
					object_latitude = location.latitude
					object_longitude = location.longitude
				except:
					geolocator = GoogleV3()
					location = geolocator.geocode(object_address)
					object_latitude = location.latitude
					object_longitude = location.longitude					
				db_item = Flat(item_type, date, metro_station, object_address, rooms, area, floor, href, source, name, object_latitude, object_longitude)
				db_session.add(db_item)
				db_session.commit()
				counter += 1
		else:
			break

def write_to_db_two(data_list):
	for item in data_list:
		link = item["href"]
		item_check = db_session.query(Flat.href, Flat.id).filter(Flat.href==link).first()
		price = item["price"]
		date = datetime.strptime(item["date"],"%d-%m-%Y %H:%M:%S")
		flat_id = item_check[1]
		db_item = Price(flat_id, price, date)
		# db_session.execute("DELETE FROM price WHERE rowid NOT IN (SELECT min(rowid) FROM price GROUP BY price, date, flat_id)")
		db_session.add(db_item)
		db_session.commit()

#сначала попробуй прогнать все позиции - если заблокируют, то попробуй работать порциями

if __name__ == "__main__":
	# data_list = out_of_file("cian_items.json") 
	data_list = out_of_file("cian_data.json")
	write_to_db_one(data_list,1)
	# write_to_db_one(data_list,25001)
	# write_to_db_one(data_list,50001)
	# write_to_db_one(data_list,75001)
	# write_to_db_one(data_list,100001)
	# write_to_db_one(data_list,125001)
	write_to_db_two(data_list)
