from flask import Flask, abort, request, render_template
from flask_bootstrap import Bootstrap
import datetime as dt
from app.irr_.IO_Ldr import out_of_file
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from app.migrations.d_base import Item, Date_and_price, db_session
from sqlalchemy import desc
from dateparser import parse
import sys

sys.path.insert(0,'migrations/items_data.sqlite')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migrations/items_data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

# def paginate(sa_query, page, per_page=20, error_out=True):
#   sa_query.__class__ = BaseQuery
#   return sa_query.paginate(page, per_page, error_out)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/real_estate")
def real_estate():
	data = Item.query.filter(Item.id).paginate(page,20, error_out = False)
	#data = db.session.query(Item).filter(Item.id).limit(20)
	number_of_items = data.count()
	date_of_retrieval = db.session.execute("SELECT date_of_parsing FROM date_and_price WHERE date_of_parsing < date('now') ORDER BY date_of_parsing DESC LIMIT 1").first()
	date_of_retrieval = (parse(str(date_of_retrieval))).strftime('%d-%m-%Y') if date_of_retrieval else None
	# #number_of_items = db.session.query(Item).filter(Item.id).limit(20).count()
	# date_and_price = db.session.query(Date_and_price).filter(Date_and_price.id).limit(20)
	# return render_template('real_estate.html', data = data, date_and_price = date_and_price, number_of_items = number_of_items, 
	# 	date_of_retrieval = date_of_retrieval)
	return render_template ('real_estate.html', data = data.items, number_of_items = number_of_items,
		date_of_retrieval = date_of_retrieval)

@app.route('/about_us')
def about_us():
	return render_template('about_us.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500

if __name__ == "__main__":
	app.run(port=5001,debug = True)