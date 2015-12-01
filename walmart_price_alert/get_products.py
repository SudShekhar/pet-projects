import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'walmart_price_alert.settings')
import sys
import django
django.setup()
import pdb
from wali.models import Product, Review
import urllib2
import pytz
import json
import HTMLParser
from datetime import datetime
#script to be run once a day
API_KEY = "a5dhwav8gzqbgh2q8gwnr728"
def add_review(product_id, title, reviewer, content, up_votes, down_votes, rating, review_time):
	defaults = {
			'up_votes':1,
			'down_votes':2,
			'content' : "aas",
			'rating':5
		}
	product_id = Product.objects.get(id=product_id)
	r, created = Review.objects.get_or_create(product_id=product_id, title=title,reviewer=reviewer,
			review_time=review_time, defaults=defaults)
	r.up_votes = up_votes
	r.down_votes = down_votes
	r.content = content
	r.rating = rating
	r.save()
	print "Added review", product_id.name
	return r.id

def add_product(name, product_id,msrp, sale_price, short_description,long_description,
		medium_image_url,large_image_url, product_url, customer_rating,customer_rating_image, available_online):
	defaults = {'name': 'random',
			'msrp':2,
			'sale_price':1.05,
			'short_description': "no",
			'long_description':"yes",
			'medium_image_url':'http://facebook.com/my.png',
			'large_image_url': "http://facebook.com/my.png",
			'product_url':"http://c.affil.walmart.com/t/api02?l=http%3A%2F%2Fwww.walmart.com%2Fip%2FSCEPTRE-X405BV-FHDR-40-LED-Class-1080P-HDTV-with-ultra-slim-metal-brush-bezel-60Hz%2F27608624%3Faffp1%3D7InOm6OAOOxup3p-Vnkefh7i7BvTPDJjWjGHcI0c9Z0%26affilsrc%3Dapi%26veh%3Daff%26wmlspartner%3Dreadonlyapi",
			'customer_rating':'5',
			'customer_rating_image':'http://facebook.com/my.png',
			'available_online':False
			}
	htmlparser = HTMLParser.HTMLParser()
	p , created = Product.objects.get_or_create(product_id=product_id,defaults=defaults)
	p.name = name
	p.msrp = msrp
	p.sale_price = sale_price
	p.short_description = htmlparser.unescape(short_description)
	p.long_description = htmlparser.unescape(long_description)
	p.medium_image_url = medium_image_url
	p.large_image_url = large_image_url
	p.product_url = product_url
	p.customer_rating = customer_rating
	p.customer_rating_image = customer_rating_image
	p.available_online = available_online
	if created:
		p.number_of_wishlists = 0
	p.save()
	return p.id

class SearchAPI:
	def __init__(self, query_term, fmt="json"):
		self.url = "http://api.walmartlabs.com/v1/search?query="+query_term+"&apikey="+API_KEY+"&format="+fmt+"&responseGroup=full"
	
	def store_in_db(self):
		json_data = self.get_json(self.url)
		total_items = json_data["totalResults"]
		total_items = 2
		print "Adding %s products" % total_items
		start = 1
		while start < total_items:
			if start !=1:
				url = self.url+"&start="+str(start)
				json_data = self.get_json(url)
			try:
				for item in json_data["items"]:
					try:
						product_id = add_product(item["name"], item["itemId"],item.get("msrp",-1), item["salePrice"], item["shortDescription"],item['longDescription'], item["mediumImage"],item['largeImage'],item["productUrl"], item["customerRating"], item['customerRatingImage'],item["availableOnline"])
						self.add_reviews(item["itemId"], product_id)
					except:
						e = sys.exc_info()[:0]
						print e
					print "Added ",item["name"]
				start = min(total_items, start+json_data["numItems"])
			except:
				print json_data
		print "OK"

	def get_json(self,url):
		try:
			response = urllib2.urlopen(url)
			html = response.read()
			json_data = json.loads(html)
		except:
			print "Couldn't get json from ",url
			json_data={}
		return json_data

	def add_reviews(self, itemId, product_id):
		url = "http://api.walmartlabs.com/v1/reviews/{0}?format=json&apiKey={1}".format(str(itemId), API_KEY)
		json = self.get_json(url)
		if json== {}:
			print "No Reviews"
			return
		try:
			for review in json["reviews"][:1]:
					print review["submissionTime"]
					try:
						review["submissionTime"] =str(pytz.utc.localize(datetime.strptime(review["submissionTime"],"%Y-%m-%dT%H:%M:%S")))
						print review["submissionTime"]
						add_review(product_id, review["title"],review["reviewer"],review["reviewText"], review["upVotes"],
							review["downVotes"], review["overallRating"]["rating"], review["submissionTime"])
					except Exception as e:
						print e
						print "Couldn't add review for : ", str(product_id)
						print sys.exct_info()[0]
						pass
		except:
			print sys.exct_info()[0]
			pass
		return


s = SearchAPI("electronics")
s.store_in_db()

