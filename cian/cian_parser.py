import requests
from bs4 import BeautifulSoup

#here we define the function that gets data - use it with every loaded page

#this is list where we store date
data_list = []

#this function gets data from a single HTML page
def parse(url):
	 r = requests.get(url)
	 soup = BeautifulSoup(r.content, "html.parser")
	 data = soup.find_all("div", {"class": "serp-item__content"})
	 for item in data:
	 	try:
	 		metro_station = item.find_all("div", {"class": "serp-item__solid serp-item__metro"})[0].text
	 		distance = item.find_all("div", {"class": "serp-item__distance"})[0].text
	 		address = item.find_all("div", {"class": "serp-item__address-precise"})[0].text
	 		price = item.find_all("div", {"class": "serp-item__price-col"})[0].text
	 		room_no = item.find_all("div", {"class": "serp-item__type-col"})[0].text
	 		area = item.find_all("div", {"class": "serp-item__area-col"})[0].text
	 		floor = item.find_all("div", {"class": "serp-item__floor-col"})[0].text
	 		data_list.append({
		 		"station": metro_station.replace("\n",""),
		 		"distance": distance.replace("\t","").replace("\n",""),
		 		"address": address.replace("\t","").replace("\n",""),
		 		"price": price.replace("\t","").replace("\n","").replace(" ","").replace("/",""),
		 		"rooms": room_no.replace("\t","").replace("\n","").replace(" ",""),
		 		"area": area.replace("\t","").replace("\n","").replace(" ",""),
		 		"floor": floor.replace("\t","").replace("\n","").replace(" ","")
		 		})
	 	except IndexError:
	 		pass
	 print(data_list)
	 
#this function sends data from the list to CSV file
def send_to_txt(some_list):
	for item in some_list:
		row_text = item.get("station")  + ";" + item.get("distance") + ";" + item.get("address") + ";" + item.get("price") + ";" + item.get("rooms") + ";" \
		+ item.get("area") + ";" + item.get("floor") + ";"
		with open("parsing_results.csv","a", encoding = "utf-8") as row:
			row.write(row_text + "\n")

#this function gets data from multiple pages
def multi_parsing(pages):
	page = 1
	while page <= pages:
		url = "http://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p=" + str(page) + "&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1&type=4"
		parse(url)
		page += 1

if __name__ == "__main__":
	multi_parsing(2)
	send_to_txt(data_list)

	

