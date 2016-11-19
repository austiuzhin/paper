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

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migrations/items_data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


@app.route("/")
def index():
	return render_template('index.html')

@app.route('/real_estate/', defaults={'page': 1})
@app.route('/real_estate', defaults={'page': 1})
@app.route('/real_estate/page/<int:page>/')
@app.route('/real_estate/page/<int:page>')
def real_estate(page = 1):
	search = False	
	page, per_page, offset = page, 20, 0
	data = db.session.query(Item).filter(Item.id).limit(int(per_page)).offset(int(offset))
	date_and_price = db.session.query(Date_and_price).filter(Date_and_price.id).limit(int(per_page)).offset(int(offset))
	total = db.session.query(Item).filter(Item.id).count()
	date_of_retrieval = db.session.execute("SELECT date_of_parsing FROM date_and_price WHERE date_of_parsing < date('now') ORDER BY date_of_parsing DESC LIMIT 1").first()
	date_of_retrieval = (parse(str(date_of_retrieval))).strftime('%d-%m-%Y') if date_of_retrieval else None
	return render_template('real_estate2.html',
                           data=data,
                           page = page,
                           per_page = per_page,
                           date_of_retrieval = date_of_retrieval, 
                           date_and_price=date_and_price)                           
	#date_of_retrieval = db.session.execute("SELECT date_of_parsing FROM date_and_price WHERE date_of_parsing < date('now') ORDER BY date_of_parsing DESC LIMIT 1").first()
	#date_of_retrieval = (parse(str(date_of_retrieval))).strftime('%d-%m-%Y') if date_of_retrieval else None
	#date_and_price = db.session.query(Date_and_price).filter(Date_and_price.id).limit(20)
	# return render_template ('real_estate.html', data = data, number_of_items = number_of_items,
	# 	date_of_retrieval = date_of_retrieval, date_and_price=date_and_price)

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