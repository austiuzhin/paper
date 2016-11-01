from create_db import db_session, Flats
import json
import codecs

def out_of_file(filename):
	with codecs.open(filename,'r','cp1251') as f_opened:
		return json.load(f_opened)

def check(data_list)
	if 

# использовать квадратные скобки

def write_to_db_one(data_list):
	for item in data_list:
		item_type = item.["type"]
		date = item.get["date"]
		metro_station = item["metro_station"]
		obj_address = item.["obj_address"]
		rooms = item.get["rooms"]
		area = item.get["area"]
		floor = item.get["floor"]
		href = item.get["href"]
		source = item.get["source"]
		name = item.get["name"]
		db_item = Flat(item_type, date, metro_station, object_address, rooms, area, floor, href, source, name)
		db_session.add(db_item)
		db_session.commit()

def write_to_db_two(data_list):
	for item in data_list:
		price = item.["name"]
		db_item = Price(price)
		db_session.add(db_item)
		db_session.commit()


if __name__ == "__main__":
	data_list = out_of_file("cian_items.json") 
	write_to_db(data_list)   

