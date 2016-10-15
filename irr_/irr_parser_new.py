import re
import requests
from bs4 import BeautifulSoup as bs_
from IO_Ldr import into_file_

links_for_parser = ['http://irr.ru/real-estate/apartments-sale/',
					'http://irr.ru/real-estate/rooms-sale/',
					'http://irr.ru/real-estate/rent/',
					'http://irr.ru/real-estate/rooms-rent/']

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
	try:
		name = (lambda x: x.text.strip())(s_data.find("h1",{"itemprop":"name"}))
	except:
		name = 'Name is not received'
	
	try:
		characteristics = list()
		char_Block_list = s_data.find_all("div",{"class":"productPage__characteristicsBlock"})[0]
		for item in range(len(char_Block_list.contents)):
			if char_Block_list.contents[item] != '\n':
				characteristics.append(re.sub('\W+','',(char_Block_list.contents[item].span.text)))
		about_flat_dict = {id_:value for (id_,value) in enumerate(characteristics)}
	except:
		about_flat_dict = {"0": "Flat chracteristics not found. Probably this is not flat."}
	try:
		about_flat_tags_list = s_data.find_all("div",{"class":"productPage__infoColumnBlock"})[0]
		about_building_tags_list = s_data.find_all("div",{"class":"productPage__infoColumnBlock"})[1]

		more_data_about_flat_dict = {id_:value for (id_,value) in enumerate([item.text.strip() for item in (about_flat_tags_list.find_all("li",{"class":"productPage__infoColumnBlockText"}))])}
		more_data_about_building_dict = {id_:value for (id_,value) in enumerate([item.text.strip() for item in (about_building_tags_list.find_all("li",{"class":"productPage__infoColumnBlockText"}))])}
	except:
		more_data_about_flat_dict, more_data_about_building_dict = {'0':'No more data about apartment.'},{'0':'No more information about building.'}
	try:
		adress = (s_data.find("div",{"class":"productPage__infoTextBold js-scrollToMap"})).text.strip()
	except:
		adress = 'Adress is not received'
	
	try:
		price = (lambda x: float(re.search('[0-9]+',x.text.strip()).group(0)))(s_data.find("div",{"class":"productPage__price js-contentPrice"}))
	except:
		price = float(0)
	
	try:
		date = (s_data.find("div",{"class":"updateProduct"})).text.strip()
		date_updated = re.sub('\W+','', date)
	except:
		date_updated = 'Date is not received'

	return name, adress, about_flat_dict, more_data_about_flat_dict, more_data_about_building_dict, price, date_updated


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
		test_item_f_cnt = 0
		for j in range(len(item_list_base_link)):			
			into_file_({id_:value for (id_,value) in enumerate(item_parser(item_list_base_link[j]))})
			test_item_f_cnt +=1
			if test_item_f_cnt == 3:
				break
		print ('First page retreived')
		page_num = 1
		for num in range(2,51):			
			if page_num == 3:
				break
			page_num += 1
			work_link = (base_link + 'page' + str(num) + '/')
			item_list_work_link = urls_for_items(work_link)			
			print ('Parsing page № '+ str(page_num) + '...')
			test_item_cnt = 0
			for k in range(len(item_list_work_link)):
				into_file_({id_:value for (id_,value) in enumerate(item_parser(item_list_work_link[k]))})
				test_item_cnt +=1
				if test_item_cnt == 3:
					break
			print ('Page № '+ str(page_num) + ' retreived')

	#for item in result:
	#	into_file_(item)

	print ("\n\nTest file saved succesfully.")

if __name__ == "__main__":
	main()