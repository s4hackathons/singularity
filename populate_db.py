import json
import uuid
from pymongo import MongoClient
from datetime import date, timedelta, datetime
from random import randint
import jtail as jt

def main():
	uid1 = uuid.uuid4()
	uid1_urn = uid1.urn
	uid1_str = uid1_urn
	uid1_str = uid1_str[9:]
	uid2 = uuid.uuid4()
	uid2_urn = uid2.urn
	uid2_str = uid2_urn
	uid2_str = uid2_str[9:]
	uid1_str = "iit2011035"
	uid2_str = "iit2011102"
	ret1 = jt.retailer(uid1_str, "dexter")
	ret2 = jt.retailer(uid2_str, "james")
	bf1 = jt.buying_frequency(uid1_str)
	bf2 = jt.buying_frequency(uid2_str)
	mongo_client = jt.mongo()
	mongo_client.insert("id_collection", ret1)
	mongo_client.insert("id_collection", ret2)
	mongo_client.insert("buying_frequency", bf1)
	mongo_client.insert("buying_frequency", bf2)

	post = mongo_client.retreive("id_collection",{"customer_name": "dexter"})
	for p in post:
		print p
	post = mongo_client.retreive("id_collection",{"customer_name": "james"})
	for p in post:
		print p
	d = date.today() - timedelta(30)

	items_json={}
	with open("items.json") as data:
		items_json = json.load(data)
	item_list = []

	for item in items_json["items"]:
		item_list.append(item)
	print item_list
	for num in range(1,30):
		new_date = d + timedelta(num)
		r = randint(0, len(item_list)-1)

		item1 = dict()
		for i in range(0,r):
			j = randint(0, len(item_list)-1)
			qt = randint(0,100)
			item1[item_list[j]] = qt

		or1 = jt.order(uid1_str,new_date.strftime('%y-%m-%d'),item1)
		r = randint(0, len(item_list)-1)

		item2 = dict()
		for i in range(0,r):
			j = randint(0, len(item_list)-1)
			qt = randint(0,100)
			item2[item_list[j]] = qt

		or2 = jt.order(uid2_str,new_date.strftime('%y-%m-%d'),item2)
		mongo_client.insert("order",or1)
		mongo_client.insert("order",or2)
		#mongo_client.update_buying_frequency(uid1_str, or1)
		#mongo_client.update_buying_frequency(uid2_str, or2)
	#post = mongo_client.retreive("order",{"id": "2734126e-f467-4e41-ab24-f49f661ec713"})
	#for p in post:
	#	print p



	print "==================================================="
	print "==================================================="
	#for i in range (0,20):
	#	pp = dict()
	#	pp["saop"] = 50
	#	mongo_client.insert("order", order("88328134-0670-479e-bac0-18fab605f4c1","16-04-10",pp))
	#	mongo_client.update_buying_frequency("88328134-0670-479e-bac0-18fab605f4c1", order("88328134-0670-479e-bac0-18fab605f4c1","16-04-10",pp))
        mongo_client.recommend({"id":"0f8a466a-d29a-43f1-bbdf-4d83b3cf44fa"})

if __name__ == "__main__":
	    main()