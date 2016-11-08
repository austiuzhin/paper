from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
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
    obj_adress = Column(String(250))
    metro_station = Column(String(150))
    rooms = Column(Integer)
    area = Column(Float)
    href = Column(String(500))#, unique = True)
    source = Column(String(50))
    floor = Column(Integer)
    relashion_btw_date_price_object = relationship('Date_and_price', backref ='rel_date_price')

    def __init__ (self, obj_type = None, name = None, obj_adress = None, metro_station = None, rooms = None, area = None, href = None, source = None, floor = None):
        self.obj_type = obj_type
        self.name = name
        self.obj_adress = obj_adress
        self.metro_station = metro_station
        self.rooms = rooms
        self.area = area
        self.href = href
        self.source = source
        self.floor = floor

    def __repr__(self):
        return '<Object  {} {} {} {}'.format(self.obj_type, self.obj_adress, self.href, self.source)

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
        return '<Price {}, creation date {}, parsing date {}>'.format(self.price,self.date_of_creation, self.date_of_parsing)

if __name__ == '__main__':
    Base.metadata.create_all(bind = engine)
