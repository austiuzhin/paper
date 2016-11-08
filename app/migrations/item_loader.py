from paar.app.irr_.IO_Ldr import out_of_file
from d_base import db_session, Item, Date_and_price
from os.path import isfile
from subprocess import call
import datetime
import re


class Loading_parsed_data(object):
    
    def __init__(self, list_with_data, db_exist = False):
        self.list_with_data = list_with_data
        self.db_exist = db_exist


    def chek_db_existance(self, dbname = './items_data.sqlite'):
        if isfile(dbname):
            self.db_exist = True

    def test_item_before_adding(self, item):
        if (item['rooms'] != None) and (item['area'] != None) and (item['floor'] != None):
            if type(item['floor']) == list:
                rooms_int = item['rooms']
                area_int = item['area']
                floor_test = item['floor']
                floor_int = floor_test[0] if (type(floor_test) == list) else None
            elif ('м2' in item['area'])  or ('м2' in item['rooms']):
                rooms_test = re.findall('[0-9.]+',item['rooms'])
                rooms_int = rooms_test[0] if rooms_test else None
                area_test = re.findall('[0-9.]+', item['area'])
                area_int = area_test[0] if area_test else None
                floor_int = item['floor']
            else:
                rooms_int = item['rooms']
                area_int = item['area']
                floor_int = item['floor']
        else:
            rooms_int = None
            area_int = None
            floor_int = None

        return rooms_int, area_int, floor_int
    
    def adding_items_to_db(self, data):
        for obj in range(len(data)-1):
            rooms_int, area_int, floor_int = self.test_item_before_adding(data[obj])
            
            _object = Item(data[obj]['type'], data[obj]['name'], data[obj]['obj_adress'],
                data[obj]['metro_station'], rooms_int, area_int, data[obj]['href'],
                data[obj]['source'], floor_int)
            db_session.add(_object)

        db_session.commit()

    def addding_price_data_to_db(self, data):        
        for est in range(len(data)-1):
            _item = Item.query.filter(Item.href == data[est]['href']).first()
            dt_pr = Date_and_price(data[est]['price'],datetime.datetime.strptime(data[est]['date'], '%d-%m-%Y'), 
                datetime.datetime.strptime(data[-1], '%d-%m-%Y %H:%M:%S'), _item.id)
            db_session.add(dt_pr)

        db_session.commit()

    def db_load(self):        
        if self.db_exist == False:
            print ('Creating database structure...')
            call('python d_base.py', shell=True)
            print ('\nImporting data from .json file...')
            self.adding_items_to_db(self.list_with_data)            
            self.addding_price_data_to_db(self.list_with_data)
            print ('Data import completed succesfully.')
        else:
            print ('\nUpdating database...')
            for obj in range(len(data)-1):                
                _item = Item.query.filter(Item.href == data[obj]['href']).first()
                rooms_int, area_int, floor_int = self.test_item_before_adding(data[obj])
                
                if _item is None:
                    _object = Item(data[obj]['type'], data[obj]['name'], data[obj]['obj_adress'],
                        data[obj]['metro_station'], rooms_int, area_int, data[obj]['href'],
                        data[obj]['source'], floor_int)
                    db_session.add(_object)
                    _item = Item.query.filter(Item.href == data[obj]['href']).first()
                    dt_pr = Date_and_price(data[obj]['price'],datetime.datetime.strptime(data[obj]['date'], '%d-%m-%Y'), 
                            datetime.datetime.strptime(data[-1], '%d-%m-%Y %H:%M:%S'), _item.id)                                        
                    db_session.add(dt_pr)
                else:
                    _item = Item.query.filter(Item.href == data[obj]['href']).first()
                    dt_pr = Date_and_price(data[obj]['price'],datetime.datetime.strptime(data[obj]['date'], '%d-%m-%Y'), 
                            datetime.datetime.strptime(data[-1], '%d-%m-%Y %H:%M:%S'), _item.id)
                    db_session.add(dt_pr)
            db_session.commit()

            print ("\nDatabase updated.")

if __name__ == '__main__':
    data = out_of_file('../irr_/items_.json')
    loader = Loading_parsed_data(data)
    loader.chek_db_existance()
    loader.db_load()