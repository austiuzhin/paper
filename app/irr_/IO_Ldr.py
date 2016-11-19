#-*-coding: UTF-8 -*-
import codecs
import json
from os.path import isfile
import csv
#from sys import stdin
import re

def read_proxie_list(filename):
    if isfile(filename):
        with open(filename,'r',encoding = 'utf-8') as f:
            proxie_string =  f.read()
        proxie_list = (proxie_string).split('\n')
        proxies = dict()
        for item in range(len(proxie_list)):
            proxies.update({'http{}'.format(item):'{}'.format(proxie_list[item])})  
        return proxies
    else:
        return 'File not found'

def into_file_(dict_ = dict()):
    try:
        type(dict_) == dict
    except IOError:
        return "Input data is not a dict"
    if isfile('./items_.json'):
        with codecs.open('./items_.json','r','cp1251') as f_in:
            data = json.load(f_in)          
    
        data.update(dict_)
    
        with codecs.open('./items_.json','w','cp1251') as f_out:
            f_out.write(json.dumps(data, skipkeys = True, indent = 4))
            
    else:
        with codecs.open('./items_.json','w','cp1251') as f_out:
            f_out.write(json.dumps(dict_, skipkeys = True, indent = 4))
                

def out_of_file(filename):
    if isfile(filename):
        with codecs.open(filename,'r','cp1251') as f_opened:
            return json.load(f_opened)
    else:
        return 'File not found'

def into_json_(dict_of_dicts, filename = 'items_.json'):
    try:
        type(dict_of_dicts) == dict
    except IOError:
        return 'Input data is not a dictionary.'
    if isfile(filename):
        with codecs.open(filename,'a','cp1251') as f_out:
            f_out.write(json.dumps(dict_of_dicts, skipkeys = True, indent = 4))
    else:
        with codecs.open(filename,'w','cp1251') as f_out:
            f_out.write(json.dumps(dict_of_dicts, skipkeys = True, indent = 4))

def append_record(record):
    with open('items_.json', 'a') as f:
        json.dump(record, f)
        f.write(os.linesep)

def csv_in_file_(dict_):
    try:
        type(dict_) == dict
    except IOError:
        return "Input data isn't a dict"
    if isfile('items_.csv'):
        with codecs.open('items_.csv','a+','utf-16') as csv_file:
            writer = csv.writer(csv_file, delimiter = ';')
            for key, value in dict_.items():
                writer.writerow((key,value))
    else:
        with codecs.open('items_.csv','w','utf-16') as csv_file:
            writer = csv.writer(csv_file, delimiter = ';')
            for key, value in dict_.items():
                writer.writerow((key,value))
            
def out_of_csv(filename):
    with codecs.open(filename,'r','cp1251') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        return [row for row in reader]
#test = stdin.readline()#input('Введи приветствие: ')
#print (add_phrase(test))


if __name__ == "__main__":
    into_file_()