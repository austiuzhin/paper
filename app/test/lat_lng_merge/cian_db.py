# from sqlalchemy import create_engine, MetaData, 
# from sqlalchemy import Column, Integer, String, Table, Float
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Engine to the database to query the data from
# source_engine = create_engine('sqlite:///blog.sqlite', echo=True)
# SourceSession = sessionmaker(source_engine)

# # Engine to the database to store the results in
# #dest_engine = create_engine('sqlite:///items_data.sqlite', echo=True)
# dest_engine = create_engine('sqlite:///:memory:', echo=True)
# DestSession = sessionmaker(dest_engine)

# # Create some toy table and fills it with some data
# Base = declarative_base()

# class Latlng(Base):
#     __tablename__ = 'latlng'
#     id = Column(Integer, primary_key=True)
#     object_latitude = Column(Float)
#     object_longitude = Column(Float)
#     href = Column(String(500))

#     def __init__(self, object_latitude=None, object_longitude = None, href = None):
#     	self.object_latitude = object_latitude
#     	self.object_longitude = object_longitude
#     	self.href = href

# db_source = scoped_session(sessionmaker(bind=source_engine))

# Base.metadata.create_all()

# db_source.query.Lalng

# import sqlite3
# con3 = sqlite3.connect("combine.db")

# con3.execute("ATTACH 'results_a.db' as dba")

# con3.execute("BEGIN")
# for row in con3.execute("SELECT * FROM dba.sqlite_master WHERE type='table'"):
#     combine = "INSERT INTO "+ row[1] + " SELECT * FROM dba." + row[1]
#     print(combine)
#     con3.execute(combine)
# con3.commit()
# con3.execute("detach database dba")

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import json
import codecs
from datetime import datetime

engine = create_engine('sqlite:///blog.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Flat(Base):
	__tablename__ = 'flat'
	id = Column(Integer, primary_key=True)
	item_type = Column(String(2))
	metro_station = Column(String(50))
	object_address = Column(String(100))
	rooms = Column(Integer)
	area = Column(Integer)
	floor = Column(String(20))
	href = Column(String(50))
	source = Column(String(10))
	name = Column(String(100))
	object_latitude = Column(String(20))
	object_longitude = Column(String(20))
	prices = relationship("Price")
	

	def __init__(self, item_type=None, date=None, metro_station=None, object_address=None, rooms=None, area=None, floor=None,\
		href=None, source=None, name=None, object_latitude=None, object_longitude=None):
		self.item_type = item_type
		self.date = date
		self.metro_station = metro_station
		self.object_address = object_address
		self.rooms = rooms
		self.area = area
		self.floor = floor
		self.href = href
		self.source = source
		self.name = name
		self.object_latitude = object_latitude
		self.object_longitude = object_longitude

	def __repr__(self):
		return '<Item {} {}>'.format(self.name, self.href)


class Price(Base):
	__tablename__ = 'price'
	id = Column(Integer, primary_key=True)
	flat_id = Column(Integer, ForeignKey('flat.id'))
	price = Column(Integer)
	date = Column(DateTime)
	
	def __init__(self, flat_id=None, price=None, date=None):
		self.flat_id = flat_id
		self.price = price
		self.date = date

	def __repr__(self):
		return '<Item {} {} processed on {}>'.format(self.id, self.price, self.date)


if __name__ == "__main__":
	Base.metadata.create_all(bind=engine)