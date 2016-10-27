import re
import requests
from bs4 import BeautifulSoup as bs_
from IO_Ldr import into_json_, out_of_csv, out_of_file
from datetime import datetime as dt_
from dateparser import parse


def urls_for_items(url,proxie):
	data = requests.get(url, proxies = proxie)
	s_data = bs_(data.text, 'lxml')
	return [item.get('href') for item in s_data.find_all("a",{"class":"listing__itemTitle js-productListingProductName"})]

def retrieving_last_possible_page(url,proxie):
	data = requests.get(url, proxies = proxie)
	s_data = bs_(data.text, 'lxml')
	list_of_pages_from_pagination = s_data.find_all("a",class_=re.compile('esLink'))
	last_page_from_pagination = list_of_pages_from_pagination[-1].text if len(list_of_pages_from_pagination) != 0 else None
	return int(last_page_from_pagination) if last_page_from_pagination else None


def retrieving_additional_information_about_object_from_description(parsed_data,type_of_object):
	object_characteristics_tags = parsed_data.find('span',class_=re.compile('Value'))
	if object_characteristics_tags != None:
		object_characteristics_tags = parsed_data.find_all('span',class_=re.compile('Value'))  
	
		number_finder = re.compile('[0-9.]+')
		if len(object_characteristics_tags) == 3:			
			number_of_rooms = object_characteristics_tags[0].text
			total_space = number_finder.search(object_characteristics_tags[1].text).group(0)
			list_with_information_about_floors = number_finder.findall(object_characteristics_tags[2].text)
			if len(list_with_information_about_floors) == 2:
				floor_number, total_number_of_floors = list_with_information_about_floors
			else:
				floor_number, total_number_of_floors = list_with_information_about_floors, None
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
			list_with_information_about_floors = number_finder.findall(object_characteristics_tags[3].text)
			if len(list_with_information_about_floors) == 2:
				floor_number, total_number_of_floors = list_with_information_about_floors
			else:
				floor_number, total_number_of_floors = list_with_information_about_floors, None
			return {
			'number_of_rooms':number_of_rooms, 
			'total_space':total_space,
			'living_space':living_space,
			'floor_number':floor_number, 
			'total_number_of_floors':total_number_of_floors,
			}		
		elif len(object_characteristics_tags) == 2:
			number_of_rooms = object_characteristics_tags[0].text
			list_with_information_about_floors = number_finder.findall(object_characteristics_tags[1].text)
			if len(list_with_information_about_floors) == 2:
				floor_number, total_number_of_floors = list_with_information_about_floors
			else:
				floor_number, total_number_of_floors = list_with_information_about_floors, None
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
	elif (object_characteristics_tags == None) and (parsed_data.status_code != 404):
		name_node = parsed_data.find("h1",{"itemprop":"name"})

		retrieving_rooms = re.match('[0-9]', name_node.text.strip())
		number_of_rooms_received_from_description = retrieving_rooms.group(0) if retrieving_rooms else None

		retrieving_floors = re.findall(u'этаж\s+([0-9/\\\\.]*)',name_node.text.strip())
		information_about_floors_received_from_description = retrieving_floors[0] if len(retrieving_floors) !=0 else None

		if information_about_floors_received_from_description and ('/' in information_about_floors_received_from_description):
			floor_number, total_number_of_floors = information_about_floors_received_from_description.split('/')
		else:
			floor_number, total_number_of_floors = None, None
		
		if type_of_object == 'RS':
			if ('квартира' in name_node.text.strip()) and ('продажи' in name_node.text.strip()):
				total_space_received_from_description = re.findall('квартира\s+([0-9/\\\\.,]+)',name_node.text.strip())[0]
				living_space_received_from_description = re.findall('продажи\s+([0-9/\\\\.,]+)',name_node.text.strip())[0]
			elif 'квартира' in name_node.text.strip():
				total_space_received_from_description = re.findall('квартира\s+([0-9/\\\\.,]+)',name_node.text.strip())[0]
				living_space_received_from_description = None
			elif 'продажи' in name_node.text.strip():
				total_space_received_from_description = None
				living_space_received_from_description = re.findall('продажи\s+([0-9/\\\\.,]+)',name_node.text.strip())[0]			
			else:
				total_space_received_from_description = None
				living_space_received_from_description = None

			return {
				'number_of_rooms':number_of_rooms_received_from_description, 
				'total_space':total_space_received_from_description,
				'living_space':living_space_received_from_description,
				'floor_number':floor_number, 
				'total_number_of_floors':total_number_of_floors,
			}

		elif type_of_object == 'RR' or type_of_object == 'AR':
			testing_if_space_is_available = re.findall('([0-9.]+)+\s+кв',name_node.text.strip())
			if testing_if_space_is_available:
				total_space_received_from_description = re.findall('([0-9.]+)+\s+кв',name_node.text.strip())[0]
				living_space_received_from_description = re.findall('([0-9.]+)+\s+кв',name_node.text.strip())[0]
			else:
				total_space_received_from_description = None
				living_space_received_from_description = None
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
	 	return (dt_.datetime.now()).strftime("%d-%m-%Y")
	else:
		updated_date = None
		created_date = None

	updated_date = (parse(updated_date)).strftime("%d-%m-%Y") if updated_date else None
	created_date = (parse(created_date)).strftime("%d-%m-%Y") if created_date else None

	return created_date if created_date else updated_date


def item_parser(url,estate_type,proxie):
	data = requests.get(url,proxies = proxie)
	s_data = bs_(data.text, 'lxml')
	metro_stations = out_of_csv('metro_.csv')
	name_node = s_data.find("h1",{"itemprop":"name"})
	try:
		additional_information_about_object_in_item = retrieving_additional_information_about_object_from_description(s_data,estate_type)
	except IOError:
		additional_information_about_object_in_item = None
	metro_description = s_data.find("div",class_=re.compile('_metro-'))
	metro_station_near_object = None
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
			'type':estate_type,
			'obj_adress':adress_description.text.strip() if adress_description else None,
			'metro_station':metro_station_near_object,
			'name': name_node.text.strip() if name_node else None,
			'area': additional_information_about_object_in_item.get('total_space') if additional_information_about_object_in_item else None,
			'rooms': additional_information_about_object_in_item.get('number_of_rooms') if additional_information_about_object_in_item else None,
			'floor': additional_information_about_object_in_item.get('floor_number') if additional_information_about_object_in_item else None,			
			'price':price,
			'href':url,
			'source':'irr',
			'date':date,
			}
	

def main():
	
	links_for_parser = [('http://irr.ru/real-estate/apartments-sale/', 'AS'),
					('http://irr.ru/real-estate/rooms-sale/', 'RS'),
					('http://irr.ru/real-estate/rent/', 'AR'),
					('http://irr.ru/real-estate/rooms-rent/', 'RR')]
	prx = out_of_file('proxies.json')
	result = []	
	print ("Started retrieving pages...\n\n")
	link_cnt = 0
	print ('I have {} links'.format(len(links_for_parser)))
	for link in range(len(links_for_parser)):
		link_cnt +=1
		print ('Parsing link № {}...'.format(link_cnt))
		base_link = links_for_parser[link][0]
		print (base_link)		
		item_list_from_base_link = urls_for_items(base_link,prx) 
		last_page_from_pagination =	retrieving_last_possible_page(base_link,prx)	 
		print ("Total number of pages is {}".format(last_page_from_pagination))
		print ("First page...")
		try:
			for j in range(len(item_list_from_base_link)):			
				result.append(item_parser(item_list_from_base_link[j],links_for_parser[link][1],prx))				
			print ('First page retreived')
		except IOError:
			break
		page_counter = 1
		try:
			for num in range(page_counter+1,last_page_from_pagination+1):			
				if page_counter == last_page_from_pagination+1:
					break
				page_counter += 1
				work_link = '{}{}{}{}'.format(base_link,'page',num,'/')
				print (work_link)
				item_list_work_link = urls_for_items(work_link,prx)			
				print ('Parsing page № {}...'.format(page_counter))
				#test_item_cnt = 0
				item_cnt = 0
				try:
					for k in range(len(item_list_work_link)):
						print ('Parsing item № {}...'.format(item_cnt))
						print (item_list_work_link[k])
						result.append(item_parser(item_list_work_link[k],links_for_parser[link][1],prx))
						item_cnt +=1
					print ('Page № {} retreived\n'.format(page_counter))
				except IOError:
					print ("Information about objects has been obtained until the position № {}".format(item_cnt))
					break
		except IOError:
			print ("Pages has been obtained until page № {}".format(page_counter))
			break
	result.append((dt_.now()).strftime("%d-%m-%Y %H:%M:%S"))
	into_json_(result)

	print ("\nFile saved succesfully.")

if __name__ == "__main__":
	main()