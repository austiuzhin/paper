import requests
from bs4 import BeautifulSoup

#here we define the function that gets data - use it with every loaded page

#this is list where we store date
data_list = []

#this function gets data from a single HTML page
def parse(url):
	 r = requests.get(url)
	 soup = BeautifulSoup(r.content, "html.parser")
	 data = soup.find_all("div", href = True)
	 for item in data:
	 	try:
	 		tag = item.get("href")
	 		print(tag)
	 		data_list.append({
	 			"tag": tag
		 		})
	 	except IndexError:
	 		pass
	 # print(data_list)
	 

#this function sends data from the list to CSV file
def send_to_txt(some_list):
	for item in some_list:
		row_text = item.get("tag") #item.get("station")  + ";" + item.get("distance") + ";" + item.get("address") + ";" + item.get("price") + ";" + item.get("rooms") + ";" \
		# + item.get("area") + ";" + item.get("floor") + ";"
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

	

