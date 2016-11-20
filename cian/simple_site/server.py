from flask import Flask, abort, request, render_template
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
import datetime as dt
from json_to_db import out_of_file


app = Flask(__name__)

bootstrap = Bootstrap(app)

@app.route("/", methods=["GET", "POST"])
def index():
	return render_template('index.html')


@app.route("/real_estate/")
def real_estate():
	data = out_of_file('cian_items.json')
	return render_template('real_estate.html', data = data)


@app.route("/results/", methods=["POST"])
def results():
	if request.method == "POST":
		print(request.form)
		data = out_of_file('cian_items.json')
		data = data[:5]
		return render_template('results.html', data = data)


@app.route('/about_us/')
def about_us():
	return render_template('about_us.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500

if __name__ == "__main__":
	app.debug = True
	app.run(port=5001,debug = True)