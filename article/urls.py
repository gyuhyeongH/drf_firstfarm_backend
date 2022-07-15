from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ArticleView.as_view(), name='article_view'),

    path('detail/', views.ArticleDetailView.as_view()),
    path('detail/<article_id>', views.ArticleDetailView.as_view()),

    path('detail/apply/<article_id>', views.ArticleApplyView.as_view()),
]