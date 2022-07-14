from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
path('', views.ArticleView.as_view(), name='article_view'),
]