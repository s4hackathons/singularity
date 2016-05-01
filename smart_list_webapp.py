from flask import Flask, render_template, request, redirect, url_for, abort, session
import json
import jtail as jt
from datetime import date, timedelta, datetime

app = Flask(__name__)

items_json={}
with open("items.json") as data:
	items_json = json.load(data)

user_id=""

@app.route('/recommend', methods=['POST', 'GET'])
def recommend_list():
	global user_id
	mongo_retrieve = jt.mongo()
	recommend_item = mongo_retrieve.recommend({"id":user_id})
	return render_template('recommend.html', recommend_list=recommend_item)

@app.route('/confirm', methods=['POST', 'GET'])
def order_placed():
	global user_id

	qty = request.form.getlist('qty')
	items = request.form.getlist('item')
	order_placed = dict()
	for i in range(len(qty)):
		if (int(qty[i]) != 0):
			order_placed[items[i]] = qty[i]
	
	print order_placed
	print user_id

	ord = jt.order(user_id, date.today().strftime('%y-%m-%d'), order_placed)

	mongo_insert = jt.mongo()
	mongo_insert.insert("order",ord)
	return "Your order has beeen placed. Thank you for using Smart List app."

@app.route('/', methods=['POST', 'GET'])
def home_page():
	if request.method == 'POST':
		global user_id
		user_id = request.form["uid"]
		print user_id
		return render_template('shopping.html', items_json=items_json)
	
	if request.method == 'GET':
		return render_template('login.html')


if __name__ == '__main__':
	app.run(debug=True)
