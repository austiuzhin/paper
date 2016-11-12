import requests
import json
import codecs
from datetime import datetime 
from bs4 import BeautifulSoup
import math

station_list = [1,100,101,102,103,104,105,106,107,108,109,10,110,111,112,113,114,115,115,116,117,118,11,119,120,121,122,123,124,\
125,126,127,128,12,129,130,131,132,133,134,135,136,137,138,13,139,140,141,142,143,144,145,146,147,148,14,149,150,151,152,153,154,\
155,156,157,158,15,159,228,229,233,234,235,236,237,238,239,16,240,243,244,245,270,271,272,273,274,275,17,281,282,283,284,285,286,\
287,18,19,2,20,21,22,23,24,25,26,27,28,29,3,30,31,32,33,34,35,36,37,38,39,4,40,41,42,43,44,45,46,47,48,49,5,50,51,52,53,54,55,56,\
57,58,59,6,60,61,62,63,64,65,66,67,68,69,7,70,71,72,73,74,75,76,77,78,79,8,80,81,82,83,84,85,86,87,88,89,8,90,91,92,93,94,95,96,97,98,99,9]

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
	 	parse_date = datetime.now().strftime("%d-%m-%Y")
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
		
	 return flat_list


def send_to_json(some_list):
	with codecs.open('cian_data.json','a','cp1251') as f_out:
			f_out.write(json.dumps(some_list, indent = 4))

#this function gets data from multiple pages
def multi_parsing(station):
	page_rent = 1
	url_rent = "http://www.cian.ru/cat.php?deal_type=rent&engine_version=2&metro%5B0%5D=" + str(station) + "&offer_type=flat&p=" + str(page_rent) + "&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1&type=4"
	pages = page_count(url_rent)
	while page_rent <= pages:
		url = "http://www.cian.ru/cat.php?deal_type=rent&engine_version=2&metro%5B0%5D=" + str(station) + "&offer_type=flat&p=" + str(page_rent) + "&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1&type=4"
		parse_rent(url)
		page_rent += 1
	
	page_sale = 1
	url_sale = "http://www.cian.ru/cat.php?deal_type=sale&engine_version=2&metro%5B0%5D=" + str(station) + "&offer_type=flat&p=" + str(page_sale) + "&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1"
	pages = page_count(url_sale)
	while page_sale <= pages:   
		url = "http://www.cian.ru/cat.php?deal_type=sale&engine_version=2&metro%5B0%5D=" + str(station) + "&offer_type=flat&p=" + str(page_sale) + "&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1"
		parse_sale(url)
		page_sale += 1
	return flat_list

def page_count(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	ads_no = (soup.find_all("div", {"class": "serp-above__count"})[0].text.split(" "))[0]
	pages_no = math.ceil(float(ads_no)/50)
	return pages_no

def parse_stations(some_list):
	for item in some_list:
		station = str(item)
		multi_parsing(station)
		print("станция {}".format(station))
	return flat_list


if __name__ == "__main__":
	flat_list = []
	# multi_parsing(1)
	# print(flat_list)
	# flat_list = []
	parse_stations(station_list)
	# # print(flat_list)
	send_to_json(flat_list)
	# page_count("http://www.cian.ru/cat.php?deal_type=rent&engine_version=2&metro%5B0%5D=244&offer_type=flat&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1&type=4")

	

