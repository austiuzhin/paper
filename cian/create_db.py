from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import codecs
from datetime import datetime

engine = create_engine('sqlite:///blog.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Flats(Base):
    __tablename__ = 'flats'
    id = Column(Integer, primary_key=True)
    item_type = Column(String(2))
    date = Column(String(20))
    metro_station = Column(String(50))
    object_address = Column(String(100))
    price = Column(Integer)
    rooms = Column(Integer)
    area = Column(Integer)
    floor = Column(String(20))
    href = Column(String(50))
    source = Column(String(10))
    name = Column(String(100))

    def __init__(self, item_type=None, date=None, metro_station=None, object_address=None, price=None, rooms=None, area=None, floor=None, href=None, source=None, name=None):
        self.item_type = item_type
        self.date = date
        self.metro_station = metro_station
        self.object_address = object_address
        self.price = price
        self.rooms = rooms
        self.area = area
        self.floor = floor
        self.href = href
        self.source = source
        self.name = name

    def __repr__(self):
        return '<Item {} {}>'.format(self.name, self.href)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)