from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'index/', views.index, name='index'),
    url(r'about/', views.about, name='about'),
    url(r'info/', views.info, name='info'),
    # url(r'list/', views.list, name='list'),
    url(r'show/(\d+)/', views.show, name='show/(\d+)/'),
    url(r'^bash/$', views.bash, name='bash'),
    url(r'^pagetitle/', views.pagetitle, name='pagetitle'),
    url(r'^searchform/', views.searchform, name='searchform/'),



]
