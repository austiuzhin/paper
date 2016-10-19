import re
import requests
from bs4 import BeautifulSoup as bs_

def move_deep(url_):
	data = requests.get(url_)
	s_data = bs_(data.text,'lxml')
	next_depth_url = s_data.find(href="/real-estate/").get('href')
	if type(next_depth_url) == str:
		return next_depth_url
	else:
		return 'Link not found'

def apartments_sale(url_):
	data = requests.get(url_)
	s_data = bs_(data.text, 'lxml')
	url_apartments = s_data.find(href=str(url_[:-1])+"/apartments-sale/").get('href')
	url_rooms = s_data.find(href=str(url_[:-1])+"/rooms-sale/").get('href')
	return url_apartments, url_rooms

def apartments_rent(url_):

#def next_page_urls(url_):
#	data = requests.get(url_)
#	s_data = bs_(data.text, 'lxml')
#	if 'page' in str(url_):
#		return [item.get('href') for item in s_data.find_all("a",{"class":"pagination__pagesLink"}) if 'page' in item.get('href')][:-1]
#	else:



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

	#living_rooms, sq_meters_whole, sq_meters_for_living, floor = characteristics # this is the furst try. 
																				  #When page is not a flat, 
																				  #for example, it is a room for 
																				  #rent or room for selling - this part gives 
																				  #a misteke. 
																				  #So, I've decided to create a dictionary and 
																				  #return all possible data in it.

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
		#price = (lambda x: float(re.search('[0-9]+',x.text.strip()).group(0)))(s_data.find("div",{"class":"productPage__price js-contentPrice"}))
		price = float((re.compile(r"[+-]?\d+(?:\.\d+)?")).search(re.sub('\W+','',s_data.find("div", class_=re.compile('_price')).text)).group(0))
	except:
		price = float(0)
	
	try:
		date = (s_data.find("div",{"class":"updateProduct"})).text.strip()
		#print (date)
		#date_updated, date_created = re.findall('([0-9]\s+\S+)\W+\S+\s+([0-9]+\s+\S+)',date)[0]
		#date_updated = re.findall('([0-9]\s+\S+)\W+',date)
		date_updated = re.sub('\W+','', date)
		#print (date_updated)
	except:
		date_updated = 'Date is not received'

	return name, adress, about_flat_dict, more_data_about_flat_dict, more_data_about_building_dict, price, date_updated#, date_created


def main():
	result = []	
	print ("Started retrieving pages...\n\n")
	real_estate = move_deep('irr.ru')


	urls_retrieved = [urls_for_items('http://irr.ru/real-estate/rent/')]#,
						#urls_for_items('http://irr.ru/real-estate/apartments-sale/'),
						#urls_for_items('http://irr.ru/real-estate/rooms-sale/')]
	
	for item in range(len(urls_retrieved)):
		
		cnt = 0
		for obj in range(len(urls_retrieved[item])):
			print ("Received urls...work on url № " + str(cnt+1))
			if cnt < 6:
				result.append({cnt:[item_parser(urls_retrieved[item][obj])]})
				cnt +=1
			else:
				break

	#result.append(item_parser('http://irr.ru/real-estate/apartments-sale/new/3-komn-kvartira-advert608863508.html'))

	for item in result:
		print (item)

	print ("\nTest finished.")

				


		

































'''

	for item in range(len(links_for_parser)):			
		for page_N in range(3):
			if 'page' not in work_link:
				link_cnt += 1
				print ( "Link № " + str(link_cnt))
				work_link = links_for_parser[item]
				next_link = page_generator(work_link)
				page_cnt = 0
				urls_retrieved = urls_for_items(work_link)
				print ("First page...")
				for obj in range(len(urls_retrieved[item])):
					print ("Received urls...work on url № " + str(page_cnt+1))
					print (urls_retrieved[item])
					if page_cnt < 3:
						#print ({page_cnt:[item_parser(urls_retrieved[obj])]})
						#result.append({page_cnt:[item_parser(urls_retrieved[obj])]})
						page_cnt +=1
					else:
						work_link = next(next_link)
						break
			else:
				print ("Next page...")
				urls_retrieved = urls_for_items(work_link)
				for obj in range(len(urls_retrieved[item])):
					print ("Received urls...work on url № " + str(page_cnt+1))
					print (urls_retrieved[item])
					if page_cnt < 3:
						result.append({page_cnt:[item_parser(urls_retrieved[obj])]})
						page_cnt +=1
					else:
						work_link = next(next_link)
						break
		

		for item in result:
			print (item)
		print (sum(1 for _ in link_generator))
	
	print ('\nTest run finished')

	#urls_retrieved = [urls_for_items('http://irr.ru/real-estate/rent/')]#,
						#urls_for_items('http://irr.ru/real-estate/apartments-sale/'),
						#urls_for_items('http://irr.ru/real-estate/rooms-sale/')]
	for item in range(len(urls_retrieved)):		
		cnt = 0
		for obj in range(len(urls_retrieved[item])):
			print ("Received urls...work on url № " + str(cnt+1))
			if cnt < 6:
				result.append({cnt:[item_parser(urls_retrieved[item][obj])]})
				cnt +=1
			else:
				break

	#result.append(item_parser('http://irr.ru/real-estate/apartments-sale/new/3-komn-kvartira-advert608863508.html'))

	for item in result:
		print (item)

	print ("\nTest finished.")
'''
if __name__ == "__main__":
	main()
