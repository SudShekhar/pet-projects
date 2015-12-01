import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'walmart_price_alert.settings')
import sys
import django
django.setup()
from wali.models import Discount, Product
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
class ManageDiscount():
    def __init__(self):
        pass
    def record(self, text):
        try:
            f = open("/home/shekhar/Documents/github/walmart_price_alert/manage_discounts.log", "aw")
            f.write(text)
            f.write("\n")
            f.close()
        except:
            pass
    def run(self):
        discounts = Discount.objects.all()
        for discount in discounts:
            self.record("Checking Deal {0} ".format(discount.product_id.name))
            if (discount.end_date <= timezone.now()+timedelta(hours=5, minutes=30)):
                self.record("Deal {0} ended ".format(discount.product_id.name))
                if discount.customers_needed() == 0:
                    body="""
                        Hi {0},
                        We are glad to tell you that the deal {1} has been confirmed.
                        Your product will be delivered to you as soon as possible.

                        Thank you.
                        Regards,
                        Walmart Requests
                        """
                    subject = "Deal Confirmed"
                    self.record("Deal confirmed")
                else:
                    body="""
                    Hi {0},
                    We are sorry but the deal on <b>{1}</b> has not passed. We will refund you your money soon.
                    Thank you.

                    Regards,
                    Walmart Requests
                    """
                    subject = "Deal Cancelled"
                    self.record("Deal rejected")
                for user in discount.waiting_users.all():
                    send_mail(subject, body.format(user.username,discount.product_id.name),"walmartrequests@gmail.com",
                        [user.email],fail_silently=False)
                discount.waiting_users.clear()
                discount.delete()
                self.record("=====================")
