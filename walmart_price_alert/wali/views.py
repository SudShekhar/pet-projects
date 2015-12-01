from django.shortcuts import render
import urllib2
import json
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from wali.models import Product, Discount
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wali.forms import OwnUserForm
from django.contrib.auth.models import User
from wali.utils import get_query
from django.utils import timezone
import re
from wali.forms import DiscountForm
import pytz
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def index(request):
    product_list = Product.objects.all()
    discounted_product_list = [d.product_id for d in Discount.objects.all()[:4]]
    query_string = ""
    found_entries = None
    if 'search' in request.GET and request.GET['search'].strip():
        query_string = request.GET['search']
        entry_query = get_query(query_string, ['name', 'short_description'])
        found_entries = Product.objects.filter(entry_query).order_by('-number_of_wishlists')
        product_list = found_entries
    paginator = Paginator(product_list, 20)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    top_items = Product.objects.order_by('-number_of_wishlists')[:4]
    best_rated = Product.objects.order_by('-customer_rating')[:3]
    context_dict = {'products' : products, 'top_items' : top_items,'best_rated':best_rated, 'found_entries': found_entries, 'query_string':query_string, 'discounted_product_list': discounted_product_list}
    return render(request, 'wali/index.html', context_dict)

@login_required
def view_product(request):
    product = Product.objects.get(product_id= request.GET["product_id"])
    reviews = product.review_set.all()
    current_user = request.user
    context_dict = {'product' : product}
    try:
        discount = product.discount
        if( discount.id != None and timezone.now() + timedelta(hours=5, minutes=30) < discount.end_date and timezone.now() + timedelta(hours=5, minutes=30) > discount.start_date):
                context_dict['discount'] = discount
        else:
            context_dict['discount'] = None
    except ObjectDoesNotExist:
        print "Product has no discount"
        context_dict['discount'] = None
    waiting_users = product.users.all()
    if(current_user in waiting_users):
        context_dict["added"] = True
    else:
        context_dict["added"] = False
    if (current_user in product.comparing_users.all()):
        context_dict["in_compare"] = True
    else:
        context_dict["in_compare"] = False
    if current_user.has_perm('add_discount'):
            context_dict["add_discount_perm"] = True
    else: context_dict["add_discount_perm"] = False
    context_dict["current_url"] = request.build_absolute_uri()
    context_dict['reviews'] = reviews
    return render(request, 'wali/view_product.html', context_dict)

@login_required
def add_to_wishlist(request):
    current_user = request.user
    if "product_id" in request.POST:
        product_id = request.POST["product_id"]
        product = Product.objects.get(product_id = product_id)
        product.users.add(current_user)
        product.number_of_wishlists = len(product.users.all())
        product.save()
    else:
        product_id = request.POST["remove_product_id"]
        product = Product.objects.get(product_id = product_id)
        product.users.remove(current_user)
        product.number_of_wishlists = len(product.users.all())
        product.save()
    url = reverse('view_product')+"?product_id="+str(product_id)
    return HttpResponseRedirect(url)

def faq(request):
    return render(request, 'wali/faq.html',{})

@login_required
def edit_user(request):
    instance = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = OwnUserForm(request.POST, instance = instance)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('index'))
        else:
            print form.errors
    else:
        form = OwnUserForm(None, instance=instance)
    return render(request, 'wali/edit_user.html',{'form':form})

def is_manager(user):
    return user.groups.filter(name='Manager').exists() or user.has_perm('wali.add_discount')

@login_required
@user_passes_test(is_manager)
def add_discount(request):
    if request.method == "POST":
        product = Product.objects.get(product_id = request.POST["product_id"])
        discount = Discount(product_id=product, start_date = request.POST["start_date"] , end_date =request.POST["end_date"], discounted_cost= request.POST["discount_price"], min_customers=request.POST["min_customers"], bought_by=0)
        discount.save()
        url = reverse("view_product")+"?product_id="+str(product.product_id)
        return HttpResponseRedirect(url)
    return reverse("index")

@login_required
@user_passes_test(is_manager)
def show_discounts(request):
    discounts = Discount.objects.all()
    return render(request,"wali/show_discounts.html", {'discounts':discounts})

@login_required
@user_passes_test(is_manager)
def delete_discount(request, discount_id):
    d = Discount.objects.get(id=discount_id)
    d.delete()
    return HttpResponseRedirect(reverse('show_discounts'))

@login_required
@user_passes_test(is_manager)
def edit_discount(request, discount_id):
    d = Discount.objects.get(id=discount_id)
    if request.method == "POST": 
        form = DiscountForm(request.POST, instance=d)
        if form.is_valid():
                form.save(commit=True)
                return HttpResponseRedirect(reverse('show_discounts'))
        else:
            print form.errors
    else:
        form = DiscountForm(None, instance=d)
    print d.start_date
    return render(request,"wali/edit_discount.html", {'discount':d, 'form':form})

@login_required
def buy_product(request, product_id):
    product = Product.objects.get(product_id=product_id)
    if not hasattr(product, 'discount') or product.discount.bought_by >= product.discount.min_customers:
        pass
    else:
        discount = product.discount
        discount.bought_by += 1
        discount.waiting_users.add(request.user)
        discount.save()
        body = """
            Hi {0},

            Thank you for buying {1}. We are waiting for {2} more users to buy the product. We will let you know the moment the deal is validated. 
            Wondering what you can do to help? You can inform others about this deal and encourage them to buy it too. The more users who buy the product, the faster our deal becomes active. 
            Thank you!

            Regards,
            Walmart Requests
            """
        send_mail("Thank you for buying",body.format(request.user.username, product.name, discount.min_customers - discount.bought_by) ,"walmartrequests@gmail.com", [request.user.email], fail_silently=True)
    return HttpResponseRedirect(product.product_url)

@login_required
def add_to_compare(request):
    if request.method == "POST":
        if "product_id" in request.POST:
            product = Product.objects.get(product_id=request.POST["product_id"])
            product.comparing_users.add(request.user)
            product.save()
        else:
            product = Product.objects.get(product_id=request.POST["remove_from_compare"])
            product.comparing_users.remove(request.user)
            product.save()
        if 'return_url' in request.GET:
            return HttpResponseRedirect(request.GET['return_url'])
        url = reverse("view_product")+"?product_id="+str(product.product_id)
        return HttpResponseRedirect(url)
    return index

@login_required
def view_compare(request):
    products = request.user.compare.all()
    context_dict = {'products' : products}
    return render(request,'wali/view_compare.html', context_dict)


