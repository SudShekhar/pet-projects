import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'walmart_price_alert.settings')
import sys
import django
django.setup()
from wali.models import Product, Valueday, Valuehour
from django.contrib.auth.models import User
import urllib2
import json
from datetime import datetime
from django.core.mail import send_mail
import HTMLParser
import StringIO
import gzip
import logging
import pdb
from django.core.urlresolvers import reverse
#script to be run once a day
API_KEY = "a5dhwav8gzqbgh2q8gwnr728"

def send_emails(product, list_type):
    users = product.users.all()
    subject = "%s is now available at discount" % product.name
    body="""
    Hi,{0}

    Walmart has listed <b>{1}</b> on the {3} list.
    Be quick and grab your purchase right away"

    Thank you.
    Regards,
    Walmart requests
    """
    url = reverse('view_product')+"?product_id="+str(product.product_id)
    for user in users:
        try:
            send_mail(subject, body.format(user.username,product.name,url, list_type),"walmartrequests@gmail.com",
                [user.email],fail_silently=False)
            logging.info("sent email to {0}".format(user.username))
        except Exception as e:
            logging.error("Exception occured : {0} while mailing {1}".format(type(e),user.email))

debug = False

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
    p.short_description = short_description
    p.long_description = htmlparser.unescape(long_description)
    p.medium_image_url = medium_image_url
    p.large_image_url = large_image_url
    p.product_url = product_url
    p.customer_rating = customer_rating
    p.customer_rating_image = customer_rating_image
    p.available_online = available_online
    if created:
        p.number_of_wishlists = 0
        user = User.objects.get(id=1)
        p.users.add(user)
    p.save()
    return p.id


class SpecialFeedsAPI:
        urls = {
            "vod":"http://api.walmartlabs.com/v1/vod?format=json&apiKey={0}".format(API_KEY),
            "voh" :"http://api.walmartlabs.com/v1/voh?apiKey={0}".format(API_KEY),
            "rollback":"http://api.walmartlabs.com/v1/feeds/rollback?format=json&apikey={0}".format(API_KEY),
            "clearance":"http://api.walmartlabs.com/v1/feeds/clearance?format=json&apikey={0}".format(API_KEY),
            "special_buy":"http://api.walmartlabs.com/v1/feeds/specialbuy?format=json&apikey={0}".format(API_KEY)
            }

        def __init__(self,feed_type, query_term="",categoryID=""):
            self.url = self.urls[feed_type]
            self.name = feed_type
            if query_term:
                self.url += "&query="+query_term
            if categoryID:
                self.url += "&categoryID"+categoryID
            logging.info("{0} api started".format(feed_type))
            logging.info("Url being used: {0}".format(self.url))

        def save_to_file(self,data, name):
            f = open(name,"w")
            f.write(data)
            f.close()

        def get_json(self,response_type ="json"):
            response = urllib2.urlopen(self.url)
            html = response.read()
            self.save_to_file(html,"raw_html")
            try:
                    if (response_type == "json"):
                        json_data = json.loads(html)
                    else:
                        data = StringIO.StringIO(html)
                        gzipper = gzip.GzipFile(fileobj=data)
                        html = gzipper.read()
                        self.save_to_file(html,"unzipped_data")
                        json_data =  json.loads(html)
            except:
                    json_data = ""
                    logging.error("Response type couldn't be converted to json")
                    logging.error("Url being used " + self.url)
            return json_data

class SingleSpecialFeeds(SpecialFeedsAPI):
    def process(self):
        json_data = self.get_json()
        item = json_data
        item_id = add_product(item["name"], item["itemId"],item.get("msrp",-1), item["salePrice"], item.get("shortDescription","No description available"),item['longDescription'], item["mediumImage"],item['largeImage'],item["productUrl"], item.get("customerRating",0), item.get('customerRatingImage',"http://me.com/1.png"),item["availableOnline"])
        if self.name == "vod":
            Valueday.objects.all().delete()
            obj = Valueday.objects.get_or_create(product_id=item_id)
            logging.info("Updated Value of day")
        else:
            Valuehour.objects.all().delete()
            obj = Valuehour.objects.get_or_create(product_id=item_id)
            logging.info("Updated Value of hour ")

        try:
            p = Product.objects.get(product_id = item["itemId"])
            logging.info(p.name + "is on discount!!")
            product_users = p.users.all()
            if product_users:
                send_emails(p,self.name)
            else:
                logging.info("%s -- No User's waiting for current discount value" % str(datetime.now()))
        except Product.DoesNotExist:
               pass

class MultipleSpecialFeeds(SpecialFeedsAPI):
    def process(self):
        json_data = self.get_json("gzip")
        if debug:
            item = json_data["items"][0]
            add_product(item["name"], item["itemId"],item.get("msrp",-1), item["salePrice"], item.get("shortDescription","No description available"),item['longDescription'], item["mediumImage"],item['largeImage'],item["productUrl"], item.get("customerRating",0), item.get('customerRatingImage',"http://me.com/1.png"),item["availableOnline"])
            logging.info("Added sample item")

        for item in json_data["items"]:
            try:
                    p = Product.objects.get(product_id = item["itemId"])
                    logging.info(p.name + "is on discount")
                    product_users = p.users.all()
                    if product_users:
                        send_emails(p,self.name)
            except Product.DoesNotExist:
                   pass

if __name__ == "__main__":
    name = sys.argv[1]
    logging.basicConfig(filename='scripts.log',level=logging.DEBUG)
    if(len(sys.argv) > 2):
        query = sys.argv[2]
    else: query = ""
    if(len(sys.argv) > 3):
        categoryID = sys.argv[3]
    else: categoryID = ""

    if name in ["rollback", "special_buy","clearance"]:
        mailer = MultipleSpecialFeeds(name,query,categoryID)
    else:
        mailer = SingleSpecialFeeds(name,query,categoryID)
    mailer.process()

