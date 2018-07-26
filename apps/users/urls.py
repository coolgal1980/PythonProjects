from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
  url(r'^$', views.index, name='index'), 
  url(r'^create$', views.create, name='create'),
  url(r'^login$', views.login, name='login'),
  # url(r'^success$', views.success),
	url(r'^logout$', views.logout, name='logout')
]