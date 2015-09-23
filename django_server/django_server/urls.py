"""diplom_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from diplom_django import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.main_window, name='main_window'),
    url(r'^routeinfrom+', views.route_infom, name='route_infom'),
    url(r'^list_route+', views.list_route, name='list_route'),
    url(r'^build_route+', views.build_route, name='build_route'),
    url(r'^addition+', views.addit_func, name='addit_func'),
    url(r'^assesment+', views.asses_func, name='asses_func'),
    url(r'^geo_map+', views.geo_map, name='geo_map'),
    url(r'^wich_days+', views.wich_days, name='wich_days'),
]
