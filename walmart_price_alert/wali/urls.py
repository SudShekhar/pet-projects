from django.conf.urls import patterns, url
from wali import views

urlpatterns = patterns('',
		url(r'^$',views.index, name ='index'),
		url(r'^view_product/',views.view_product, name='view_product'),
		url(r'^add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
		url(r'^faq/',views.faq,name='faq'),
		url(r'^edit_user/',views.edit_user, name='edit_user'),
		url(r'^add_discount/', views.add_discount, name='add_discount'),
		url(r'^show_discounts/', views.show_discounts, name='show_discounts'),
		url(r'^edit_discount/([0-9]*)/', views.edit_discount, name='edit_discount'),
		url(r'^delete_discount/([0-9]*)/', views.delete_discount, name='delete_discount'),
        url(r'^buy_product/([0-9]*)/', views.buy_product, name='buy_product'),
        url(r'^view_compare/', views.view_compare, name='view_compare'),
        url(r'^add_to_compare/', views.add_to_compare, name='add_to_compare')
		)
