#-*- coding = utf-8 -*-
#@Time : 2020/9/30 18:13
#@Author : straightup
from django.conf.urls import url, include
from api import views

urlpatterns = [
    # CBV
    url(r'^server/$', views.ServerView.as_view()),
    # FBV
    # url(r'^get_data/', views.get_data),
    # url(r'^get_server/', views.get_server),
]
