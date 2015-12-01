from django.conf.urls import patterns, include, url
from django.contrib import admin

from registration.backends.simple.views import RegistrationView
	
	# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self,request, user):
        return '/wali/'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'walmart_price_alert.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('wali.urls')),
	url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
	url(r'^aut/', include('django.contrib.auth.urls')),
	url(r'^accounts/', include('registration.backends.simple.urls') ))
