import re
import requests
from bs4 import BeautifulSoup as bs_
from IO_Ldr import into_json_, out_of_csv
from datetime import datetime as dt_
from dateparser import parse

links_for_parser = [('http://irr.ru/real-estate/apartments-sale/', 'AS'),
					('http://irr.ru/real-estate/rooms-sale/', 'RS'),
					('http://irr.ru/real-estate/rent/', 'AR'),
					('http://irr.ru/real-estate/rooms-rent/', 'RR')]

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

def urls_for_items(url):
	data = requests.get(url)
	s_data = bs_(data.text, 'lxml')
	return [item.get('href') for item in s_data.find_all("a",{"class":"listing__itemTitle js-productListingProductName"})]

def retrieving_additional_information_about_object_from_description(parsed_data,type_of_object):
	object_characteristics_tags = parsed_data.find('span',class_=re.compile('Value'))
	if object_characteristics_tags != None:
		object_characteristics_tags = parsed_data.find_all('span',class_=re.compile('Value'))  
	
		number_finder = re.compile('[0-9.]+')
		if len(object_characteristics_tags) == 3:			
			number_of_rooms = object_characteristics_tags[0].text
			total_space = number_finder.search(object_characteristics_tags[1].text).group(0)
			floor_number, total_number_of_floors = number_finder.findall(object_characteristics_tags[2].text)
			return {
			'number_of_rooms':number_of_rooms, 
			'total_space':total_space, 
			'floor_number':floor_number, 
			'total_number_of_floors':total_number_of_floors,
			}
		elif len(object_characteristics_tags) == 4:
			number_of_rooms = object_characteristics_tags[0].text
			total_space = number_finder.search(object_characteristics_tags[1].text).group(0)
			living_space = number_finder.search(object_characteristics_tags[2].text).group(0)
			floor_number, total_number_of_floors = number_finder.findall(object_characteristics_tags[3].text)
			return {
			'number_of_rooms':number_of_rooms, 
			'total_space':total_space,
			'living_space':living_space,
			'floor_number':floor_number, 
			'total_number_of_floors':total_number_of_floors,
			}		
		elif len(object_characteristics_tags) == 2:
			number_of_rooms = object_characteristics_tags[0].text
			floor_number, total_number_of_floors = number_finder.findall(object_characteristics_tags[1].text)
			return {
			'number_of_rooms':number_of_rooms, 		
			'floor_number':floor_number, 
			'total_number_of_floors':total_number_of_floors,
			}		
		else:		
			return {
			'number_of_rooms':None, 
			'total_space':None,
			'living_space':None,
			'floor_number':None, 
			'total_number_of_floors':None,
			}
	elif object_characteristics_tags == None:
		name_node = parsed_data.find("h1",{"itemprop":"name"})
		number_of_rooms_received_from_description = re.match('[0-9]', name_node.text.strip()).group(0)
		information_about_floors_received_from_description = re.findall(u'этаж\s+([0-9/\\\\.]*)',name_node.text.strip())[0]
		if '/' in information_about_floors_received_from_description:
			floor_number, total_number_of_floors = information_about_floors_received_from_description.split('/')
		else:
			floor_number, total_number_of_floors = None, None
		
		if type_of_object == 'RS':
			total_space_received_from_description = re.findall('квартира\s+([0-9/\\\\.,]+)',name_node.text.strip())[0]
			living_space_received_from_description = re.findall('продажи\s+([0-9/\\\\.,]+)',name_node.text.strip())[0]

			return {
				'number_of_rooms':number_of_rooms_received_from_description, 
				'total_space':total_space_received_from_description,
				'living_space':living_space_received_from_description,
				'floor_number':floor_number, 
				'total_number_of_floors':total_number_of_floors,
			}

		elif type_of_object == 'RR' or type_of_object == 'AR':
			total_space_received_from_description = re.findall('([0-9.]+)+\s+кв',name_node.text.strip())[0]
			living_space_received_from_description = re.findall('([0-9.]+)+\s+кв',name_node.text.strip())[0]
		
			return {
				'number_of_rooms':number_of_rooms_received_from_description, 
				'total_space':total_space_received_from_description,
				'living_space':living_space_received_from_description,
				'floor_number':floor_number, 
				'total_number_of_floors':total_number_of_floors,
			}
	
	else:		
		return {
		'number_of_rooms':None, 
		'total_space':None,
		'living_space':None,
		'floor_number':None, 
		'total_number_of_floors':None,
		}		
	
def date_retrieved_from_object_info(parsed_data):
	date_string = parsed_data.find("div",{"class":"updateProduct"})
	raw_date = re.sub('\W+','', date_string.text) if date_string else None
	if ('Размещено' in raw_date) and (raw_date != None):
		updated_date, created_date = raw_date.split('Размещено')
	elif ('Размещено' in raw_date) and ('сегод' in raw_date) and (raw_date != None):
		updated_date, created_date = raw_date.split('Размещено')
	elif ('Размещено' not in raw_date) and (raw_date != None):
		updated_date = raw_date
		created_date = None
	elif ('Размещено' not in raw_date) and ('сегод' in raw_date) and (raw_date != None):
	 	return (datetime.datetime.now()).strftime("%d-%m-%Y")
	else:
		updated_date = None
		created_date = None

	updated_date = parse(updated_date) if updated_date else None
	created_date = parse(created_date) if created_date else None

	return created_date if created_date else updated_date


def item_parser(url):
	data = requests.get(url)
	s_data = bs_(data.text, 'lxml')	
	est_type = real_estate_type(url)
	metro_stations = out_of_csv('metro_.csv')
	name_node = s_data.find("h1",{"itemprop":"name"})
	additional_information_about_object_in_item = retrieving_additional_information_about_object_from_description(s_data,est_type)
		
	metro_description = s_data.find("div",class_=re.compile('_metro-'))
	if metro_description:
		for item in metro_stations:
			if item[0] in metro_description.text.strip():
				metro_station_near_object = item[0]
	else:
		metro_station_near_object = None	
	
	adress_description = s_data.find("div",{"class":"productPage__infoTextBold js-scrollToMap"})
	
	num_searcher = re.compile(r"[+-]?\d+(?:\.\d+)?")
	price_from_description = s_data.find("div", class_=re.compile('_price'))
	list_of_numbers_from_string = num_searcher.findall(price_from_description.text.strip()) if price_from_description else None
	price = float(''.join(list_of_numbers_from_string))	if list_of_numbers_from_string else None
	
	date = date_retrieved_from_object_info(s_data)

	return {
			'type':est_type,
			'obj_adress':adress_description.text.strip() if adress_description else None,
			'metro_station':metro_station_near_object,
			'name': name_node.text.strip() if name_node else None,
			'area': additional_information_about_object_in_item.get('total_space'),
			'rooms': additional_information_about_object_in_item.get('number_of_rooms'),
			'floor': additional_information_about_object_in_item.get('floor_number'),			
			'price':price,
			'href':url,
			'source':'irr',
			'date':date,
			}
	

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