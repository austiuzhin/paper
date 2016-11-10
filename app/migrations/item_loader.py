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
            testing_object = Item.query.filter(Item.href == data[obj]['href']).first()
            if testing_object is None:
                _object = Item(data[obj]['type'], data[obj]['name'], data[obj]['obj_adress'],
                    data[obj]['metro_station'], rooms_int, area_int, data[obj]['href'],
                    data[obj]['source'], floor_int)
            else:
               pass
            db_session.add(_object)

        db_session.commit()

    def addding_price_data_to_db(self, data):        
        for est in range(len(data)-1):
            _item = Item.query.filter(Item.href == data[est]['href']).first()
            _item_test = Date_and_price.query.get(_item.id)                       
            dt_pr = Date_and_price(data[est]['price'],datetime.datetime.strptime(data[est]['date'], '%d-%m-%Y'), 
                datetime.datetime.strptime(data[-1], '%d-%m-%Y %H:%M:%S'), _item.id)
            if _item_test is None:
                db_session.add(dt_pr)
            else:
                if (_item_test.price, _item_test.date_of_creation, _item_test.date_of_parsing, _item_test.object_id) == (dt_pr.price, dt_pr.date_of_creation, dt_pr.date_of_parsing, dt_pr.object_id):
                    pass        
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
                    dt_pr = Date_and_price(data[obj]['price'],datetime.datetime.strptime(data[obj]['date'], '%d-%m-%Y'), 
                            datetime.datetime.strptime(data[-1], '%d-%m-%Y %H:%M:%S'), _item.id)                    
                    db_session.add(dt_pr)
            db_session.execute("DELETE FROM date_and_price WHERE rowid NOT IN (SELECT min(rowid) FROM date_and_price GROUP BY price, date_of_creation,date_of_parsing,object_id)")
            db_session.commit()

            print ("\nDatabase updated.")

if __name__ == '__main__':
    data = out_of_file('../irr_/items_.json')
    loader = Loading_parsed_data(data)
    loader.chek_db_existance()
    loader.db_load()
    #Debug functions
    # test_lst = ['../irr_/items_1.json','../irr_/items_2.json']
    # for item in test_lst:
    #     data = out_of_file(item)
    #     loader = Loading_parsed_data(data)
    #     loader.chek_db_existance()
    #     loader.db_load()