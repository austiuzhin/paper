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

def apartments_sale(url_)
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
	name = (lambda x: x.text.strip())(s_data.find_all("h1",{"class":"productPage__title js-productPageTitle productPage__title_lines_1"}))
	sq_meters_whole = (lambda x: x.text.strip())(s_data.find_all("span",{"class":"productPage__characteristicsItemValue"}))
	sq_meters_for_living = 
	floor = (lambda x: x.text.strip())(s_data.find_all("span",{"class":"productPage__characteristicsItemValue"}))
	number_of_rooms = 
	price = (lambda x: float(re.search('[0-9]+',x.text.strip()).group(0)))(s_data.find_all("div",{"class":"productPage__price js-contentPrice"}))
	about_flat_list = 
	about_building_list = 
	date = 
