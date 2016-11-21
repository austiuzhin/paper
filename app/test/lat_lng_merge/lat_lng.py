from sqlalchemy import create_engine, MetaData, 
from sqlalchemy import Column, Integer, String, Table, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Engine to the database to query the data from
source_engine = create_engine('sqlite:///blog.sqlite', echo=True)
SourceSession = sessionmaker(source_engine)

# Engine to the database to store the results in
dest_engine = create_engine('sqlite:///items_data.sqlite', echo=True)
DestSession = sessionmaker(dest_engine)

# Create some toy table and fills it with some data
Base = declarative_base()

class Latlng(Base):
    __tablename__ = 'latlng'
    id = Column(Integer, primary_key=True)
    object_latitude = Column(Float)
    object_longitude = Column(Float)
    href = Column(String(500))

    def __init__(self, object_latitude=None, object_longitude = None, href = None):
    	self.object_latitude = object_latitude
    	self.object_longitude = object_longitude
    	self.href = href

db_source = scoped_session(sessionmaker(bind=source_engine))

Base.metadata.create_all()

db_source.query.Lalng