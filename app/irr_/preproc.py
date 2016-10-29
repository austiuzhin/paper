import re
import json
import datetime
from IO_Ldr import into_json_, out_of_file

''' 
#This is an old version. I had tried to do all __in_one_line__, 
#but data which had been in files was difficult to __tighten__.

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
'''

def merging_text_names(dict_):
	for item in range(len(dict_)-1):#Объединяет текст в наименованиях
		if len(dict_[str(item)]['2']) > 1:			
			dict_[str(item)]['2'] = ('').join(dict_[str(item)]['2'])

def needed_irr_complex(dict_):
	ready_data = []
	for item in range(len(dict_)-1):
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
			rooms = re.search('^[0-9]',dict_[str(item)]['2']).group(0)
		
		floor_info = floor_search(dict_[str(item)])

		price = dict_[str(item)].get('8')
		
		href_ = dict_[str(item)].get('1')

		try:
			date_from site = date_from_site(dict_[str(item)]['9'])
		except:
			date_from site = 0

	return 


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

def date_from_site(string_):
	year = int((datetime.datetime.now()).strftime("%Y"))
	dates = {u'янв':'1',u'февр':'2',u'мар':'3',u'апр':'4',u'ма':'5',u'июн':'6',u'июл':'7',u'авг':'8',u'сент':'9',u'октяб':'10',u'нояб':'11',u'дека':'12'}
	if u'сегод' in string_:
		return (datetime.datetime.now()).strftime("%d-%m-%Y")
	else:
		months = re.findall(r'янв|февр|мар|апр|ма|июн|июл|авг|сент|октяб|нояб|дека', string_)
		for item in range(len(months)):
			months[item] = dates.get(months[item])
		days = re.findall('[+-]?\d+(?:\.\d+)?', string_)
		if len(days) == 2:
			refresh_date = (datetime.date(year,int(months[0]),int(days[0]))).strftime('%d-%m-%Y')
			creation_date = (datetime.date(year,int(months[1]),int(days[1]))).strftime('%d-%m-%Y')
			return refresh_date,creation_date
		else:
			return (datetime.date(year,int(months[0]),int(days[0]))).strftime('%d-%m-%Y')

def floor_search(dict_):
	if (len(dict_['5']) == 1):
		try:
			return re.search(u'этаж\s+[0-9]?',dict_['2']).group(0)
		except:
			return 0
	elif (len(dict_['5']) == 4) or (len(dict_['5']) == 3):
		items = range(len(dict_['5']))
		return dict_['5'][str(items[-2])] + ' этаж из ' + dict_['5'][str(items[-1])]
	elif len(dict_['5']) == 5:
		return dict_['5']['3'] +' этаж из '+ dict_['5']['4']
	else:
		return 0
			


def main():
	data = merging_text_names(out_of_file('/irr_/items_.json'))	
	ready_data = needed_irr_complex(data)
	into_json_(ready_data, filename_ = 'ready_data.json')


if __name__ == "__main__":
	# main()
	raw_date = '20сентябряРазмещено6сентября'
	if 'Размещено' in raw_date:
		updated_date, created_date = raw_date.split('Размещено')
	else:
		updated_date = raw_date
		created_date = None

	updated_date = parse(updated_date)
	created_date = parse(created_date) if created_date else None
	