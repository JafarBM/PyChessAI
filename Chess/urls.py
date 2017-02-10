from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$', home_page, name='home'),
	url(r'^login/$', login_page, name='login'),
	url(r'^signup/$', signup_page, name='signup'),
	url(r'^info_login/$', info_login, name='info_login'),
	url(r'^info_signup/$', info_signup, name='info_signup'),
	url(r'^activation/$', activation, name='activation'),
]