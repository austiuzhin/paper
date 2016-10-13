import re
import requests
from bs4 import BeautifulSoup as bs_

def move_deep(url_):
	data = requests.get(url_)
	s_data = bs_(data.text,'html.parser')
	next_depth_url = s_data.find(href="/real-estate/").get('href')
	if type(next_depth_url) == str:
		return next_depth_url
	else:
		return 'Link not found'

def apartments_sale(url_):
	data = requests.get(url_)
	s_data = bs_(data.text, 'html.parser')
	url_apartments = s_data.find(href=str(url_[:-1])+"/apartments-sale/").get('href')
	url_rooms = s_data.find(href=str(url_[:-1])+"/rooms-sale/").get('href')
	return url_apartments, url_rooms

def urls_for_items(url_):
	data = requests.get(url_)
	s_data = bs_(data.text, 'html.parser')
	return [item.get('href') for item in s_data.find_all("a",{"class":"listing__itemTitle js-productListingProductName"})]

def item_parser(url_):
	data = requests.get(url_)
	s_data = bs_(data.text, 'html.parser')
	name = (lambda x: x.text.strip())(s_data.find("h1",{"itemprop":"name"}))
	characteristics = list()
	char_Block_list = s_data.find_all("div",{"class":"productPage__characteristicsBlock"})[0]
	for item in range(len(char_Block_list.contents)):
		if char_Block_list.contents[item] != '\n':
			characteristics.append(re.sub('\W+','',(char_Block_list.contents[item].span.text)))
	living_rooms, sq_meters_whole, sq_meters_for_living, floor = characteristics

	about_flat_tags_list = s_data.find_all("div",{"class":"productPage__infoColumnBlock"})[0]
	about_building_tags_list = s_data.find_all("div",{"class":"productPage__infoColumnBlock"})[1]

	more_data_about_flat_list = [item.text.strip() for item in (about_flat_tags_list.find_all("li",{"class":"productPage__infoColumnBlockText"}))]
	more_data_about_building_list = [item.text.strip() for item in (about_building_tags_list.find_all("li",{"class":"productPage__infoColumnBlockText"}))]
	price = (lambda x: float(re.search('[0-9]+',x.text.strip()).group(0)))(s_data.find("div",{"class":"productPage__price js-contentPrice"}))
	
	date = (s_data.find("div",{"class":"updateProduct"})).text.strip()
	#print (date)
	#date_updated, date_created = re.findall('([0-9]\s+\S+)\W+\S+\s+([0-9]+\s+\S+)',date)[0]
	#date_updated = re.findall('([0-9]\s+\S+)\W+',date)
	date_updated = re.sub('\W+','', date)
	#print (date_updated)
	return name, living_rooms, sq_meters_whole, sq_meters_for_living, floor, more_data_about_flat_list,more_data_about_building_list,price,date_updated#, date_created


def main():
	result = []
	cnt = 0
	print ("Started retrieving pages...\n\n")
	urls_retrieved = urls_for_items('http://irr.ru/real-estate/rent/')
	for item in range(len(urls_retrieved)):
		if cnt < 6:
			result.append([cnt, (item_parser(urls_retrieved[item]))])
			cnt +=1
		else:
			break

	#result.append(item_parser('http://irr.ru/real-estate/apartments-sale/new/3-komn-kvartira-advert608863508.html'))

	for item in result:
		print (item)

	print ("Test finished.")

if __name__ == "__main__":
	main()
