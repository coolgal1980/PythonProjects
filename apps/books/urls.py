from django.conf.urls import url
# from views import *
from . import views  
# from django.contrib import admin

urlpatterns = [
    url(r'^home$', views.home, name = "home"),
    url(r'^add_book/$', views.add_book, name="add_book"),
    url(r'^create_review/(?P<id>\d+)$', views.create_review, name="create_review"),
    url(r'^show/(?P<id>\d+)$', views.show, name="show"),
    url(r'^user/(?P<id>\d+)$', views.user, name="user"),
    url(r'^destroy/(?P<id>\d+)$', views.destroy, name="destroy"),
    # url(r'^admin/', admin.site.urls),
]
