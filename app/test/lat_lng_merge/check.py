from cian_db import db_session as cian
from irr_db import db_session as irr
from cian_db import Flat
from irr_db import Item

def main():
	print ("Начинаю процесс анализа...")
	total = Flat.query.filter(Flat.id).count()
	for instance in range(1,total-1):
		lat = Flat.query.filter(Flat.id == instance).first().object_latitude
		lng = Flat.query.filter(Flat.id == instance).first().object_longitude
		first_href = Flat.query.filter(Flat.id == instance).first().href		
		test_item = Item.query.filter(Item.href == first_href).first()
		if test_item == None:
			continue
		id_for_insertion = test_item.id
		#Item.query.filter(Item.id == id_for_insertion).first().insert().values(lat=lat,lng=lng)
		item = Item.query.get(id_for_insertion)
		#item.update().values(lat=lat,lng=lng)
		item.lat=lat
		item.lng=lng
		#irr.add(item)
		if instance%1000 == 0:
			print ("Добавляю данные в элемент № {}".format(instance))

	print ("\nАнализ закончен.")

	irr.commit()

	print ("\nБаза данных обновлена.")


if __name__ == '__main__':
	main()