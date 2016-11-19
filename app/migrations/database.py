# It's not ready and not working.
# Here I try to refactor my DB for SQLAlchemy.
#
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migrations/items_data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

estate_items = db.Table('estate_items',
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)  
    obj_type = db.Column(db.String(5))
    name = db.Column(db.Text)
    obj_address = db.Column(db.String(250))
    metro_station = db.Column(db.String(150))
    rooms = db.Column(db.Integer)
    area = db.Column(db.Float)
    href = db.Column(db.String(250), unique = True)
    source = db.Column(db.String(50))
    floor = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    is_valid = db.Column(db.Boolean))

Date_and_price = db.Table('date_and_price',
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)  
    price = db.Column(db.Integer)
    date_of_creation = db.Column(db.DateTime)
    date_of_parsing = db.Column(db.DateTime)
    object_id = db.Column(db.Integer, db.ForeignKey('estate_items.id')))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)  
    obj_type = db.Column(db.String(5))
    name = db.Column(db.Text)
    obj_address = db.Column(db.String(250))
    metro_station = db.Column(db.String(150))
    rooms = db.Column(db.Integer)
    area = db.Column(db.Float)
    href = db.Column(db.String(250), unique = True)
    source = db.Column(db.String(50))
    floor = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    is_valid = db.Column(db.Boolean)
    
    #relashion_btw_date_price_object = relationship('Date_and_price', backref ='rel_date_price')

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
        
class Date_and_price(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)  
    price = db.Column(db.Integer)
    date_of_creation = db.Column(db.DateTime)
    date_of_parsing = db.Column(db.DateTime)
    object_id = db.Column(db.Integer, db.ForeignKey('estate_items.id'))
    

    def __init__(self, price = None, date_of_creation = None, date_of_parsing = None,  object_id = None):
        self.price = price
        self.date_of_creation = date_of_creation
        self.date_of_parsing = date_of_parsing
        self.object_id = object_id

    def __repr__(self):
        return '{} {}'.format(self.price,self.date_of_creation)
        

if __name__ == '__main__':
    db.create_all()