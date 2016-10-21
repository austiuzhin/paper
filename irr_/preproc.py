import re
import json
from IO_Ldr import into_json_, out_of_file

data = out_of_file('/irr_/items_.json')

def needed_irr_simple(dict_):
	needed = []
	for item in range(len(dict_)):
		try:
			needed.append({'0':dict_[str(item)].get('0'),
			'1':dict_[str(item)].get('3'),
			'2':dict_[str(item)].get('4'),
			'3':dict_[str(item)].get('2'),
			'4':(dict_[str(item)].get('5')).get('1'),
			'5':(dict_[str(item)].get('5')).get('0'),
			'6':(dict_[str(item)].get('5')).get('3')+' этаж из  '+(dict_[str(item)].get('5')).get('4'),
			'7':dict_[str(item)].get('8'),
			'8':dict_[str(item)].get('1'),
			'9':'irr_'})
		except:
			continue

	return needed

def merging_text_names(dict_):
	for item in range(len(dict_)-1):#Объединяет текст в наименованиях
		if len(dict_[str(item)]['2']) > 1:			
			dict_[str(item)]['2'] = ('').join(dict_[str(item)]['2'])

def needed_irr_complex(dict_):
	for item in range(len(data)-1):
		classif = dict_[str(item)].get('0')
		try:
			adress = dict_[str(item)]['3']
		except:
			adress = 0
		try:
			metro_st = dict_[str(item)]['4']
		except:
			metro_st = 0
		try:
			name = dict_[str(item)]['2']
		except:
			name = 0
		try:
			total_sq = dict_[str(item)]['5']['1']
		except:			
			total_sq = total_square_choser()
			if dict_[str(item)][str(5)][str(0)] == '02': #Если нет описания помещения
				total_sq.append(RS_or_RR_living_square(dict_[str(item)]['2']))
			if len(total_sq) == 2:
				total_sq = total_sq[1]
			else:
				pass
		try:
			rooms = dict_[str(item)]['5']['0']
		except:			
			rooms = re.search('[^0-9]',dict_[str(item)]['2']).group(0)
		
#		floor_info = dict_[str(item)]['5']['3']+' этаж из  '+(dict_[str(item)]['5']['4']
#
#		price = 
#		href_ = 
#		date_from site = 
		
			#sq_meters = re.compile(u'\s+[0-9]+\s+')
	#sq_meters.search(t_list[100]).group(0).strip()
	#for item in range(len(data)):
	#	classif = data[item].get('0')
	#	adress = data[item].get('3')
	#	metro_st = data[item].get('3')
	#	name = 
	#	total_sq = 

def RS_or_RR_living_square(string_):
	square_lst = []
	try:
		text_in_name_split = re.split(' ',string_)
		for item in range(len(text_in_name_split)):
			try:
				if (text_in_name_split[item] == u'квартира') or (text_in_name_split[item] == u'продажи') or (text_in_name_split[item] == u'комнаты'):
					square_lst.append(text_in_name_split[item+1])
			except:
					square_lst.append(0)	
		if len(square_lst) == 1:
			return float(square_lst[0])
		else:
			return float(square_lst[0]), float(square_lst[1])
	except:
		return 0