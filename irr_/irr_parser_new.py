import re
import requests
from bs4 import BeautifulSoup as bs_
from IO_Ldr import into_json_, out_of_csv
from datetime import datetime as dt_

'''
Mistakes in data_retrieval
	Name is not received - 01
	Flat chracteristics not found. Probably this is not a flat - 02
	No more data about apartment - 03
	No more information about building -04	
	No metro station nearby - 05
	Adress is not received - 06
	Date is not received - 07
	If price is equal to - 0.0 
'''
mtr_stations = out_of_csv('metro_.csv')

links_for_parser = ['http://irr.ru/real-estate/apartments-sale/',
					'http://irr.ru/real-estate/rooms-sale/',
					'http://irr.ru/real-estate/rent/',
					'http://irr.ru/real-estate/rooms-rent/']

def real_estate_type(url_):
	if 'apartments-sale' in url_:
		return 'AS'
	elif 'rooms-sale' in url_:
		return 'RS'
	elif 'rent' in url_:
		return 'AR'
	elif 'rooms-rent' in url_:
		return 'RR'
	else:
		return 'Unknown real-estate type'

def page_generator(url_):
	for num in range(2,52):
		yield url_ + 'page' + str(num) + '/'

def urls_for_items(url_):
	data = requests.get(url_)
	s_data = bs_(data.text, 'lxml')
	return [item.get('href') for item in s_data.find_all("a",{"class":"listing__itemTitle js-productListingProductName"})]

def item_parser(url_):
	data = requests.get(url_)
	s_data = bs_(data.text, 'lxml')	
	est_type = real_estate_type(url_)
	try:
		name = (lambda x: x.text.strip())(s_data.find("h1",{"itemprop":"name"}))
	except:
		name = '01'	
	try:		
		char_Block_list = s_data.find_all("div",{"class":"productPage__characteristicsBlock"})[0]
		characteristics = [re.search('[0-9.]+',(item.text.strip())).group(0) for item in char_Block_list.find_all('span',class_=re.compile('Value'))]+[re.search('[0-9]+',(char_Block_list.find('span',class_=re.compile('gray')).text)).group(0)]		
		about_flat_dict = {id_:value for (id_,value) in enumerate(characteristics)}
	except:
		about_flat_dict = {"0": "02"}
	try:
		about_flat_tags_list = s_data.find_all("div",{"class":"productPage__infoColumnBlock"})[0]
		about_building_tags_list = s_data.find_all("div",{"class":"productPage__infoColumnBlock"})[1]

		more_data_about_flat_dict = {id_:value for (id_,value) in enumerate([item.text.strip() for item in (about_flat_tags_list.find_all("li",{"class":"productPage__infoColumnBlockText"}))])}
		more_data_about_building_dict = {id_:value for (id_,value) in enumerate([item.text.strip() for item in (about_building_tags_list.find_all("li",{"class":"productPage__infoColumnBlockText"}))])}
	except:
		more_data_about_flat_dict, more_data_about_building_dict = {'0':'03'},{'0':'04'}
	try:
		mtr_string = s_data.find("div",class_=re.compile('_metro-')).text.strip()
		metro_st = [item[0] for item in mtr_stations if item[0] in mtr_string][0]
	except:
		metro_st = '05'
	try:
		adress = (s_data.find("div",{"class":"productPage__infoTextBold js-scrollToMap"})).text.strip()
	except:
		adress = '06'
	
	try:		
		price = float((re.compile(r"[+-]?\d+(?:\.\d+)?")).search(re.sub('\W+','',s_data.find("div", class_=re.compile('_price')).text)).group(0))
	except:
		price = float(0)

	try:
		date = (s_data.find("div",{"class":"updateProduct"})).text.strip()
		date_updated = re.sub('\W+','', date)
	except:
		date_updated = '07'

	return est_type, url_, name, adress, metro_st, about_flat_dict, more_data_about_flat_dict, more_data_about_building_dict, price, date_updated


def main():
	result = []	
	print ("Started retrieving pages...\n\n")
	link_cnt = 0
	print ('I have ' + str(len(links_for_parser)) + ' links' )
	for link in range(len(links_for_parser)):
		link_cnt +=1
		print ('Parsing link № ' + str(link_cnt) + '...')
		base_link = links_for_parser[link]
		print (base_link)		
		item_list_base_link = urls_for_items(base_link)		
		print ("First page...")
		#test_item_f_cnt = 0
		try:
			for j in range(len(item_list_base_link)):			
				result.append({id_:value for (id_,value) in enumerate(item_parser(item_list_base_link[j]))})
		#		test_item_f_cnt +=1
		#		if test_item_f_cnt == 3:
		#			break
			print ('First page retreived')
		except:
			break
		page_num = 1
		try:
			for num in range(2,51):			
				if page_num == 5:
					break
				page_num += 1
				work_link = (base_link + 'page' + str(num) + '/')
				item_list_work_link = urls_for_items(work_link)			
				#print ('Parsing page № '+ str(page_num) + '...')
				#test_item_cnt = 0
				item_cnt = 0
				try:
					for k in range(len(item_list_work_link)):
						result.append({id_:value for (id_,value) in enumerate(item_parser(item_list_work_link[k]))})
				#		test_item_cnt +=1
						item_cnt +=1
				#		if test_item_cnt == 3:
				#			break
					print ('Page № '+ str(page_num) + ' retreived')
				except:
					print ("Information about objects has been obtained until the position № " + str(item_cnt))
					break
		except:
			print ("Pages has been obtained until page № " + str(page_num))
			break
	result.append((dt_.now()).strftime("%d-%m-%Y %H:%M:%S"))
	into_json_({obj_id_:object_ for (obj_id_,object_) in enumerate(result)})

	print ("\nFile saved succesfully.")

if __name__ == "__main__":
	main()