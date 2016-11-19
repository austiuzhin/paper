from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
import logging

engine = create_engine('sqlite:///items_data.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

Base.query = db_session.query_property()

#Creating a logger and a log file for debugging
handler = logging.FileHandler('sqlalchemy.engine.log')
handler.level = logging.DEBUG
logging.getLogger('sqlalchemy.engine').addHandler(handler)


class Item(Base):
    __tablename__ = 'estate_items'
    id = Column(Integer, primary_key = True, autoincrement = True)  
    obj_type = Column(String(5))
    name = Column(Text)
    obj_address = Column(String(250))
    metro_station = Column(String(150))
    rooms = Column(Integer)
    area = Column(Float)
    href = Column(String(250), unique = True)
    source = Column(String(50))
    floor = Column(Integer)
    lat = Column(Float)
    lng = Column(Float)
    is_valid = Column(Boolean)
    
    relashion_btw_date_price_object = relationship('Date_and_price', backref ='rel_date_price')

    def __init__ (self, obj_type = None, name = None, obj_address = None, metro_station = None, 
        rooms = None, area = None, href = None, source = None, floor = None, lat = None, lng = None, is_valid = True):
        
        self.obj_type = obj_type
        self.name = name
        self.obj_address = obj_address
        self.metro_station = metro_station
        self.rooms = rooms
        self.area = area
        self.href = href
        self.source = source
        self.floor = floor
        self.lat = lat
        self.lng = lng
        self.is_valid = is_valid

    def __repr__(self):
        return '{} {} {} {} {} {} {} {} {} {} {}'.format(self.obj_type, self.name, self.obj_address, self.metro_station, 
            self.rooms, self.area, self.href, self.source, self.floor, self.lat, self.lng, self.is_valid)
        
class Date_and_price(Base):
    __tablename__ = 'date_and_price'
    id = Column(Integer, primary_key = True, autoincrement = True)  
    price = Column(Integer)
    date_of_creation = Column(DateTime)
    date_of_parsing = Column(DateTime)
    object_id = Column(Integer, ForeignKey('estate_items.id'))
    

    def __init__(self, price = None, date_of_creation = None, date_of_parsing = None,  object_id = None):
        self.price = price
        self.date_of_creation = date_of_creation
        self.date_of_parsing = date_of_parsing
        self.object_id = object_id

    def __repr__(self):
        return '{} {}'.format(self.price,self.date_of_creation)
        

if __name__ == '__main__':
    Base.metadata.create_all(bind = engine)
