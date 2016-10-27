import requests
import json
import codecs
from datetime import datetime 
from bs4 import BeautifulSoup

#here we define the function that gets data - use it with every loaded page

#this is list where we store date

#this function gets data from a single HTML page


def parse_rent(url):
	 r = requests.get(url)
	 soup = BeautifulSoup(r.content, "html.parser")
	 rent_data = soup.find_all("div", {"class": "serp-item__content"})
	 for item in rent_data:
	 	try:
	 		metro_station = item.find_all("div", {"class": "serp-item__solid serp-item__metro"})[0].text
	 		metro_station = metro_station.replace("\n","")
	 	except IndexError:
	 		metro_station = "Метро еще не построено"   
	 	address = item.find_all("div", {"class": "serp-item__address-precise"})[0].text
	 	price_tags = item.find_all("div", {"class": "serp-item__price-col"})
	 	price = price_tags[0].find_all("div", {"class": "serp-item__solid"})[0].text.split(" ")
	 	room_no = item.find_all("div", {"class": "serp-item__type-col"})
	 	room = room_no[0].find_all("div", {"class": "serp-item__solid"})[0].text.split("-")
	 	room = room[0].replace("\t","").replace("\n","").replace(" ","")
	 	area_total = item.find_all("div", {"class": "serp-item__area-col"})
	 	area = area_total[0].find_all("div", {"class": "serp-item__solid"})[0].text.split(" ")
	 	floor_line = item.find_all("div", {"class": "serp-item__floor-col"})
	 	floor = floor_line[0].find_all("div", {"class": "serp-item__solid"})[0].text.split(" ")
	 	try:
	 		floors = floor[0] + " этаж из " + floor[3]
	 	except IndexError:
	 		floors = floor[0] + " этаж из " + floor[0]
	 	parse_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	 	link = item.find("a",{"class":"serp-item__card-link link"}).get('href')
	 	if room == "Студия":
	 		name = "Студия, {}".format(metro_station)
	 	else:
	 		name = "{}-комнатная квартира, {}".format(room, metro_station)
	 	flat_list.append({
	 		"type": "AR",
	 		"date": parse_date,
	 		"metro_station": metro_station,
			"obj_address": address.replace("\t","").replace("\n",""),
			"price": (price[0] + price[1]).replace("\t","").replace("\n","").replace(" ","").replace("/",""),
			"rooms": room,
			"area": area[0].replace("\t","").replace("\n","").replace(" ",""),
			"floor": floors.replace("\t","").replace("\n",""),
			"href": link,
			"source": "cian",
			"name": name
			})

	 del flat_list[:3]
	 return flat_list

def parse_sale(url):
	 r = requests.get(url)
	 soup = BeautifulSoup(r.content, "html.parser")
	 sale_data = soup.find_all("div", {"class": "serp-item__content"})
	 for item in sale_data:
	 	try:
	 		metro_station = item.find_all("div", {"class": "serp-item__solid serp-item__metro"})[0].text
	 		metro_station = metro_station.replace("\n","")
	 	except IndexError:
	 		metro_station = "Метро еще не построено"
	 	address = item.find_all("div", {"class": "serp-item__address-precise"})[0].text
	 	address = address.replace("\t","").replace("\n","")
	 	price_tags = item.find_all("div", {"class": "serp-item__price-col"})
	 	price = price_tags[0].find_all("div", {"class": "serp-item__solid"})[0].text.split("млн")
	 	room_no = item.find_all("div", {"class": "serp-item__type-col"})
	 	room = room_no[0].find_all("div", {"class": "serp-item__solid"})[0].text.split("-")
	 	room = room[0].replace("\t","").replace("\n","").replace(" ","")
	 	area_total = item.find_all("div", {"class": "serp-item__area-col"})
	 	area = area_total[0].find_all("div", {"class": "serp-item__solid"})[0].text.split(" ")
	 	floor_line = item.find_all("div", {"class": "serp-item__floor-col"})
	 	floor = (floor_line[0].find_all("div", {"class": "serp-item__solid"})[0].text).strip().split(" ")
	 	try:
	 		floors = floor[0] + " этаж из " + floor[3]
	 	except IndexError:
	 		floors = floor[0] + " этаж из " + floor[0]
	 	parse_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	 	link = item.find("a",{"class":"serp-item__card-link link"}).get('href')
	 	if room == "Студия":
	 		name = "Студия, {}".format(metro_station)
	 	else:
	 		name = "{}-комнатная квартира, {}".format(room, metro_station)
	 	flat_list.append({
	 		"type": "AS",
	 		"date": parse_date,
	 		"metro_station": metro_station,
	 		"obj_address": address,
	 		"price": str(int(float(price[0].replace("\t","").replace("\n","").replace(" ","").replace("/","").replace(",",".").replace("руб",""))*1000000)),
	 		"rooms": room,
	 		"area": area[0].replace("\t","").replace("\n","").replace(" ",""),
	 		"floor": floors.replace("\t","").replace("\n",""),
	 		"href": link,
	 		"source": "cian",
	 		"name": name
	 		})
		
	 del flat_list[:3]
	 return flat_list


def send_to_json(some_list):
	with codecs.open('cian_data.json','a','cp1251') as f_out:
			f_out.write(json.dumps(some_list, indent = 4))

#this function gets data from multiple pages
def multi_parsing(pages):
	page_rent = 1
	page_sale = 1
	counter = 1
	while page_rent <= pages:
		url = "http://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p=" + str(page_rent) + "&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1&type=4"
		parse_rent(url)
		page_rent += 1
	while page_sale <= pages:   
		url = "http://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=" + str(page_sale) + "&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1&type=4"
		parse_sale(url)
		page_sale += 1
		print("страница " + str(counter))
		counter += 1

	return flat_list


if __name__ == "__main__":
	flat_list = []
	# multi_parsing(40)
	parse_rent("http://www.cian.ru/cat.php?deal_type=rent&engine_version=2&metro%5B0%5D=244&offer_type=flat&p=3&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1&type=4")
	print(flat_list)
	send_to_json(flat_list)
	

	

