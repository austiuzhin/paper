import json
import codecs

data = []

# def from_json(filename):
# 	with open(filename,'r') as some_data:
# 		data = json.load(some_data)

# from_json("cian_data.json")
# print(data)

def from_json(filename):
	with codecs.open(filename,'r','cp1251') as f_opened:
		data = json.load(f_opened)

from_json("cian_data.json")
print(data)