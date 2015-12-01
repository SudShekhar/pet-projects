from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Product(models.Model):
	name = models.CharField(max_length = 500)
	product_id = models.IntegerField(unique = True)
	msrp = models.FloatField()
	sale_price = models.FloatField()
	short_description = models.TextField()
	long_description = models.TextField()
	medium_image_url = models.URLField()
	large_image_url = models.URLField()
	product_url = models.URLField(max_length = 500)
	customer_rating = models.CharField(max_length=128)
	customer_rating_image = models.URLField(max_length=500)
	available_online = models.BooleanField(default=False)
	number_of_wishlists = models.IntegerField(default=0)
	users = models.ManyToManyField(User, related_name = "users")
        comparing_users = models.ManyToManyField(User, related_name = "compare")

	def __unicode__(self):
		return self.name

class Clearance(models.Model):
	product = models.OneToOneField(Product)

class Valueday(models.Model):
	product = models.OneToOneField(Product)

class Specialbuy(models.Model):
	product = models.OneToOneField(Product)

class Valuehour(models.Model):
	product = models.OneToOneField(Product)

class Rollback(models.Model):
	product = models.OneToOneField(Product)

class Discount(models.Model):
    product_id = models.OneToOneField(Product)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField()
    discounted_cost = models.FloatField(verbose_name= "Discounted Cost")
    min_customers = models.IntegerField(verbose_name="Minimum Number of customers")
    bought_by = models.IntegerField(verbose_name="Already brought by", default=0)
    waiting_users = models.ManyToManyField(User)
    def __unicode__(self):
		return self.product_id.name

    def customers_needed(self):
        if self.bought_by >= self.min_customers:
            return 0
        else:
            return self.min_customers -self.bought_by

class Review(models.Model):
	product_id = models.ForeignKey(Product)
	title = models.CharField(max_length=512)
	reviewer = models.CharField(max_length=512)
	content = models.TextField()
	up_votes = models.IntegerField()
	down_votes = models.IntegerField()
	rating = models.IntegerField()
	review_time = models.DateTimeField()
	
	def __str__(self):
		return self.title
