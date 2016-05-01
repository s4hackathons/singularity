import json
import uuid
from pymongo import MongoClient
from datetime import date, timedelta, datetime
from random import randint


class retailer:
	def __init__(self, id, customer_name):
		self.id = id
		self.customer_name = customer_name


class order:
	def __init__(self, id, date, items):
		self.id = id
		self.date = date
		self.items = items

	def get_item(self):
		return self.items

	def get_id(self):
		return self.id
	
	def get_date(self):
		return self.date


class buying_frequency:
	def __init__(self, id):
		self.id = id
		self.items = dict()

class mongo:
	client = MongoClient("mongodb://127.0.0.1:27017")
	db = client.recommendation
	id_collection = db.idcollection
	order = db.order
	buying_frequency = db.buying_frequency

	def __init__(self):
		print "initiated"

	def insert(self, collection_name, d):
		s = json.dumps(d, default=lambda o: o.__dict__)
		s = json.loads(s)
		if collection_name == "id_collection":
			results = self.id_collection.insert_one(s)
			print results.inserted_id
		elif collection_name == "order":
			results = self.order.insert_one(s)
			print type(d)
			self.update_buying_frequency(d.get_id(), d)
			print results.inserted_id
		elif collection_name == "buying_frequency":
			results = self.buying_frequency.insert_one(s)
			print results.inserted_id
		

	def retreive(self, collection_name, j_to_retrieve):
		if collection_name == "id_collection":
			results = self.id_collection.find(j_to_retrieve)
			print results
			return results
		elif collection_name == "order":
			results = self.order.find(j_to_retrieve)
			print results
			return results
		elif collection_name == "buying_frequency":
			print j_to_retrieve
			results = self.buying_frequency.find(j_to_retrieve)
			print results
			return results

	def recommend(self, id):
		print "inside recommend"
		print id
		p = self.retreive("buying_frequency",id)
		recommend_items = dict()
		for post in p:
			print post
			item_list = post["items"]
			for key,value in item_list.iteritems():
				freq = value["freq"]
				qty = value["qty"]
				l_pur = value["last_purchased"]
				d = date.today()
				str_d = d.strftime('%y-%m-%d')
				date1 = datetime.strptime(str_d , '%y-%m-%d')
				l_d = datetime.strptime(l_pur , '%y-%m-%d')
				delta = abs(date1 - l_d)
				if(delta.days >= freq):
						recommend_items[key] = qty
						print "KEY" + "     " + "qty"
						print key + "     " + str(qty)

		return recommend_items

	def update_buying_frequency(self, id, d):
		collection_name = "buying_frequency"
		p = self.retreive("buying_frequency",{"id":id})
		item  = d.get_item()
		for post in p:
			already_existing_keys = post["items"]
			for key, value in item.iteritems():
				if not key in already_existing_keys.keys():
					key1 = "items." + key + ".freq"
					val1 = 3
					key2 = "items." + key + ".first"
					val2 = d.get_date()
					key3 = "items." + key + ".qty"
					val3 = value
					key4 = "items." + key + ".last_purchased"
					val4 = val2
					print "first_time_entry"
					self.buying_frequency.update({"id":id},{"$set":{key1: val1, key2: val2, key3: val3, key4: val4}},upsert=True)
				else:
					ll = "items." + key
					c = self.order.count({"id":id, ll: {"$gt": 0}} )
					sum_tot = self.order.find({"id":id, ll: {"$gt": 0}} )
					sum = 0;
					for cc in sum_tot:
						print "cc is"
						print cc
						sum = sum + cc["items"][key]
					sum = sum/c
					print "sum is", sum
					date_first = already_existing_keys[key]["first"]
					date1 = datetime.strptime(date_first , '%y-%m-%d')
					cur_date = datetime.strptime(d.get_date(),'%y-%m-%d')
					print date1, "  ", cur_date
					delta = abs(date1 - cur_date)
					key1 = "items." + key + ".freq"
					val1 = int(delta.days/c)
					if val1 == 0:
						val1 = 1
					key2 = "items." + key + ".qty"
					val2 = sum
					print val1
					key4 = "items." + key + ".last_purchased"
					val4 = d.get_date()
					self.buying_frequency.update({"id":id},{"$set":{key1: val1, key2: val2, key4: val4}},upsert=True)
		p = self.retreive("buying_frequency",{"id":id})
		for post in p:
			print post