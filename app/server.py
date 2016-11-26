import sys

sys.path.insert(0,'migrations/items_data.sqlite')

from flask import Flask, abort, request, render_template
from flask_bootstrap import Bootstrap
import datetime as dt
from app.irr_.IO_Ldr import out_of_file
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from app.migrations.d_base import Item, Date_and_price
from sqlalchemy import desc
from dateparser import parse
from main.algo import get_key_for_sorting, top_five_distances,distance_matrix_walk

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migrations/items_data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)



def validatingType(variable):
    try:
        variable = int(variable)
        return variable
    except ValueError:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    with open('static/map_api_key.txt','r') as file:
        api_key = file.readline()
    return render_template('index.html', api_key=api_key)


@app.route('/real_estate/', defaults={'page': 1})
@app.route('/real_estate', defaults={'page': 1})
@app.route('/real_estate/page/<int:page>/')
@app.route('/real_estate/page/<int:page>')
def real_estate(page = 1):    
    page, per_page, offset = page, 20, 0 #вот тут сломалась пагинация, нужно, чтобы per_page и offset сдвигался на каждой новой странице
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


@app.route("/results/", methods=["POST"])
@app.route("/results", methods=["POST"])
def results():  
    if request.method == "POST":
        input_type = str(request.form['input_type'])
        input_room = validatingType(request.form['input_room'])
        input_address = str(request.form['input_address'])
        #return render_template('test.html', input_type = input_type, input_room = input_room, input_address =  input_address)
        nearest_spots_ids_list, spot_coords = top_five_distances(input_type,input_room,input_address)
        
        ins_id, distance_text, duration_text, duration_value = \
         distance_matrix_walk(nearest_spots_ids_list, spot_coords)
        data = db.session.query(Item).filter(Item.id.in_(ins_id)).all()
        total = db.session.query(Item).filter(Item.id.in_(ins_id)).count()
        #date_and_price = db.session.query(Date_and_price).filter(Date_and_price.object_id).limit(int(per_page)).offset(int(offset))
        date_and_price = db.session.query(Date_and_price).filter(Date_and_price.object_id.in_(ins_id)).all()
        date_of_retrieval = db.session.execute("SELECT date_of_parsing FROM date_and_price WHERE date_of_parsing < date('now') ORDER BY date_of_parsing DESC LIMIT 1").first()
        date_of_retrieval = (parse(str(date_of_retrieval))).strftime('%d-%m-%Y') if date_of_retrieval else None
        return render_template('results.html',
                                data=data,
                                date_of_retrieval = date_of_retrieval,
                                total = total,
                                distance_text = distance_text,
                                duration_text = duration_text,
                                date_and_price=date_and_price)
    

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