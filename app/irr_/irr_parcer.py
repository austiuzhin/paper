import re
import requests
from bs4 import BeautifulSoup as bs_


def data_retr(url_):	#Retrieving data from HTML page
	data = requests.get(url_)
	s_data = bs_(data.text,'html.parser')
	names = [(lambda x: x.text.strip())(item) for item in list(s_data.find_all("a",{"class":"listing__itemTitle js-productListingProductName"}))]
	sq_meters = [(lambda x: x.text.strip())(item) for item in list(s_data.find_all("div",{"class":"listing__itemColumn_param1"}))]
	floor = [(lambda x: x.text.strip())(item) for item in list(s_data.find_all("div",{"class":"listing__itemColumn_param2"}))]
	price = [(lambda x: float(re.search('[0-9]+',x.text.strip()).group(0)))(item) for item in list(s_data.find_all("div",{"class":"listing__itemPrice"}))]
	return names, sq_meters, floor,price
	
def json_cr(names, sq_meters, floor,price):	#Creating a dict
	items_dict = [{'name':name, 'sq_meters':sq_meters, 'floor':floor, 'price':price} for (name,sq_meters,floor,price) in zip(names, sq_meters, floor,price)]
	dict_all = {id:value for (id,value) in zip (range(len(names)),items_dict)}
	for item in dict_all.items():
		print (item)

def main():
	names, sq_meters, floor,price = data_retr('http://irr.ru/real-estate/apartments-sale/')
	json_cr(names, sq_meters, floor,price)


if __name__ == "__main__":
	main()
