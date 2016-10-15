#-*-coding: UTF-8 -*-
import codecs
import json
from os.path import isfile
import csv
#from sys import stdin
import re

def into_file_(dict_ = dict()):
	try:
		type(dict_) == dict
	except IOError:
		return "Input data isn't a dict"
	if isfile('./items_.json'):
		with codecs.open('./items_.json','r','cp1251') as f_in:
			data = json.load(f_in)
			f_in.close()
	
		data.update(dict_)
	
		with codecs.open('./items_.json','w','cp1251') as f_out:
			f_out.write(json.dumps(data, skipkeys = True, indent = 4))
			
	else:
		with codecs.open('./items_.json','w','cp1251') as f_out:
			f_out.write(json.dumps(dict_, skipkeys = True, indent = 4))
				

def out_of_file():
	if isfile('./items_.json'):
		with codecs.open('./items_.json','r','cp1251') as f_opened:
			return json.load(f_opened)
	else:
		return 'File not found'	

def csv_in_file_(dict_):
	try:
		type(dict_) == dict
	except IOError:
		return "Input data isn't a dict"
	if isfile('./items_.csv'):
		with codecs.open('./items_.csv','a+','utf-16') as csv_file:
			writer = csv.writer(csv_file, delimiter = ';')
			for key, value in dict_.items():
				writer.writerow((key,value))
	else:
		with codecs.open('./items_.csv','w','utf-16') as csv_file:
			writer = csv.writer(csv_file, delimiter = ';')
			for key, value in dict_.items():
				writer.writerow((key,value))
			

#test = stdin.readline()#input('Введи приветствие: ')
#print (add_phrase(test))


if __name__ == "__main__":
	into_file_()