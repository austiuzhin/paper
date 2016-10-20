import requests
import json
from datetime import datetime 
from bs4 import BeautifulSoup

#here we define the function that gets data - use it with every loaded page

#this is list where we store date
rent_list = []
sale_list = []
url_list = []
new_list = []

#this function gets data from a single HTML page

def get_url(url):
	 r = requests.get(url)
	 soup = BeautifulSoup(r.content, "html.parser")
	 url_data = soup.find_all("div", href = True)
	 for item in url_data:
	 	try:
	 		tag = item.get("href")
	 		url_list.append({
	 			"link": tag
		 		})
	 	except IndexError:
	 		pass
	 del url_list[:3]

def parse_rent(url):
	 r = requests.get(url)
	 soup = BeautifulSoup(r.content, "html.parser")
	 rent_data = soup.find_all("div", {"class": "serp-item__content"})
	 for item in rent_data:
	 	try:
	 		# number_d = number_d + 1
	 		metro_station = item.find_all("div", {"class": "serp-item__solid serp-item__metro"})[0].text
	 		address = item.find_all("div", {"class": "serp-item__address-precise"})[0].text
	 		price_tags = item.find_all("div", {"class": "serp-item__price-col"})
	 		price = price_tags[0].find_all("div", {"class": "serp-item__solid"})[0].text.split(" ")
	 		room_no = item.find_all("div", {"class": "serp-item__type-col"})
	 		room = room_no[0].find_all("div", {"class": "serp-item__solid"})[0].text.split("-")
	 		area_total = item.find_all("div", {"class": "serp-item__area-col"})
	 		area = area_total[0].find_all("div", {"class": "serp-item__solid"})[0].text.split(" ")
	 		floor_line = item.find_all("div", {"class": "serp-item__floor-col"})
	 		floor = floor_line[0].find_all("div", {"class": "serp-item__solid"})[0].text.split(" ")
	 		parse_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	 		rent_list.append({
		 		"type": "rent",
		 		"date": parse_date,
		 		"station": metro_station.replace("\n",""),
		 		"address": address.replace("\t","").replace("\n",""),
		 		"price": (price[0] + price[1]).replace("\t","").replace("\n","").replace(" ","").replace("/",""),
		 		"rooms": room[0].replace("\t","").replace("\n","").replace(" ",""),
		 		"area": area[0].replace("\t","").replace("\n","").replace(" ",""),
		 		"floor": (floor[0] + "/" + floor[3]).replace("\t","").replace("\n","").replace(" ","")
		 		})
	 	except IndexError:
	 		metro_station = "No data"
	 		address = item.find_all("div", {"class": "serp-item__address-precise"})[0].text
	 		price_tags = item.find_all("div", {"class": "serp-item__price-col"})
	 		price = price_tags[0].find_all("div", {"class": "serp-item__solid"})[0].text.split(" ")
	 		room_no = item.find_all("div", {"class": "serp-item__type-col"})
	 		room = room_no[0].find_all("div", {"class": "serp-item__solid"})[0].text.split("-")
	 		area_total = item.find_all("div", {"class": "serp-item__area-col"})
	 		area = area_total[0].find_all("div", {"class": "serp-item__solid"})[0].text.split(" ")
	 		floor_line = item.find_all("div", {"class": "serp-item__floor-col"})
	 		floor = floor_line[0].find_all("div", {"class": "serp-item__solid"})[0].text.split(" ")
	 		parse_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	 		rent_list.append({
	 			"type": "rent",
	 			"date": parse_date,
	 			"station": metro_station,
		 		"address": address.replace("\t","").replace("\n",""),
		 		"price": (price[0] + price[1]).replace("\t","").replace("\n","").replace(" ","").replace("/",""),
		 		"rooms": room[0].replace("\t","").replace("\n","").replace(" ",""),
		 		"area": area[0].replace("\t","").replace("\n","").replace(" ",""),
		 		"floor": (floor[0] + "/" + floor[3]).replace("\t","").replace("\n","").replace(" ","")
		 		}) 
	 del rent_list[:3]
	
def parse_sale(url):
	 r = requests.get(url)
	 soup = BeautifulSoup(r.content, "html.parser")
	 sale_data = soup.find_all("div", {"class": "serp-item__content"})
	 for item in sale_data:
	 	try:
	 		metro_station = item.find_all("div", {"class": "serp-item__solid serp-item__metro"})[0].text
	 		address = item.find_all("div", {"class": "serp-item__address-precise"})[0].text
	 		price_tags = item.find_all("div", {"class": "serp-item__price-col"})
	 		price = price_tags[0].find_all("div", {"class": "serp-item__solid"})[0].text.split("млн")
	 		room_no = item.find_all("div", {"class": "serp-item__type-col"})
	 		room = room_no[0].find_all("div", {"class": "serp-item__solid"})[0].text.split("-")
	 		area_total = item.find_all("div", {"class": "serp-item__area-col"})
	 		area = area_total[0].find_all("div", {"class": "serp-item__solid"})[0].text.split(" ")
	 		floor_line = item.find_all("div", {"class": "serp-item__floor-col"})
	 		floor = floor_line[0].find_all("div", {"class": "serp-item__solid"})[0].text.strip().split(" ")
	 		parse_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	 		sale_list.append({
		 		"type": "sale",
		 		"date": parse_date,
		 		"station": metro_station.replace("\n",""),
		 		"distance": distance.replace("\t","").replace("\n"," ").strip(" "),
		 		"address": address.replace("\t","").replace("\n",""),
		 		"price": price[0].replace("\t","").replace("\n","").replace(" ","").replace("/",""),
		 		"rooms": room[0].replace("\t","").replace("\n","").replace(" ",""),
		 		"area": area[0].replace("\t","").replace("\n","").replace(" ",""),
		 		"floor": (floor[0] + "/" + floor[3]).replace("\t","").replace("\n","").replace(" ","")
		 		})
	 	except IndexError:
	 		metro_station = "No data"
	 		distance = "No data"
	 		address = item.find_all("div", {"class": "serp-item__address-precise"})[0].text
	 		price_tags = item.find_all("div", {"class": "serp-item__price-col"})
	 		price = price_tags[0].find_all("div", {"class": "serp-item__solid"})[0].text.split("млн")
	 		room_no = item.find_all("div", {"class": "serp-item__type-col"})
	 		room = room_no[0].find_all("div", {"class": "serp-item__solid"})[0].text.split("-")
	 		area_total = item.find_all("div", {"class": "serp-item__area-col"})
	 		area = area_total[0].find_all("div", {"class": "serp-item__solid"})[0].text.split(" ")
	 		floor_line = item.find_all("div", {"class": "serp-item__floor-col"})
	 		floor = floor_line[0].find_all("div", {"class": "serp-item__solid"})[0].text.strip().split(" ")
			parse_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	 		sale_list.append({
	 			"type": "sale",
	 			"date": parse_date,
	 			"station": metro_station,
		 		"address": address.replace("\t","").replace("\n",""),
		 		"price": price[0].replace("\t","").replace("\n","").replace(" ","").replace("/",""),
		 		"rooms": room[0].replace("\t","").replace("\n","").replace(" ",""),
		 		"area": area[0].replace("\t","").replace("\n","").replace(" ",""),
		 		"floor": (floor[0] + "/" + floor[3]).replace("\t","").replace("\n","").replace(" ","")
		 		}) 
	 del sale_list[:3] 

#this function sends data from the list to CSV file
def send_data_to_csv(some_list):
	for item in some_list:
		row_text = item.get("type") + ";" + item.get("link") + ";" + item.get("station")  + ";" + item.get("distance") + ";" + item.get("address") + ";" + item.get("price") + ";" + item.get("rooms") + ";" + item.get("area") + ";" + item.get("floor") + ";"
		with open("parsing_results.csv","a", encoding = "utf-8") as row:
			row.write(row_text + "\n")


def send_to_json(some_list):
	for item in some_list:
		json.dump(item, open("cian_data.json","a"))


#this function gets data from multiple pages
def multi_parsing(pages, types):
	page = 1
	while page <= pages:
		url = "http://www.cian.ru/cat.php?deal_type=" + str(types) + "&engine_version=2&offer_type=flat&p=" + str(page) + "&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1&type=4"
		if types == "rent":
			parse_rent(url)
		elif types == "sale":
			parse_sale(url)
		get_url(url)
		page += 1


def merger(url_list, some_list):
	for item in some_list:	
		item.update(url_list[0])
		del url_list[0]


if __name__ == "__main__":
	multi_parsing(30, "rent")
	merger(url_list, rent_list)
	send_to_json(rent_list)
	multi_parsing(30, "sale")
	merger(url_list, sale_list)
	send_to_json(sale_list)
	

	

