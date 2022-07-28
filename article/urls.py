from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # article/
    path('', views.ArticleView.as_view(), name='article_view'),

    path('detail/', views.ArticleDetailView.as_view(), name='article_create_view'),
    path('detail/<article_id>', views.ArticleDetailView.as_view(), name='article_detail_view'),

    path('detail/apply/<article_id>', views.ArticleApplyView.as_view(), name='article_apply_view'),

    # user_category가 farm 인 경우의 mypage
    path('farm/', views.FarmMyPageView.as_view(), name='farm_page'),
    path('farm/<article_id>', views.FarmApplyView.as_view(), name='farm_apply_page'),

    # user_category가 farmer 인 경우의 mypage ( naming 다시 )
    path('farmer/', views.FarmerMyPageView.as_view(), name='farmer_page'),
    path('<article_id>/farmer', views.FarmerMyPageView.as_view(), name='farmer_page'),
    path('farmer/<review_id>', views.FarmerMyPageView.as_view(), name='farmer_page'),
    path('review', views.FarmerReviewView.as_view(), name='farmer_review_page'),
]