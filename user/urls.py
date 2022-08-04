from django.contrib import admin
from django.urls import path, include
from user import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # user/
    path('api/logout/', views.UserLogoutView.as_view(), name='logout'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', views.FirstFarmTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.UserView.as_view(), name='user_view'),
    path('<obj_id>/', views.UserView.as_view()),
]