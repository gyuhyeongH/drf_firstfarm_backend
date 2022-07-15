from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # article/
    path('detail/', views.ArticleDetailView.as_view()),
    path('detail/<article_id>', views.ArticleDetailView.as_view()),

    path('detail/apply/<article_id>', views.ArticleApplyView.as_view()),
]