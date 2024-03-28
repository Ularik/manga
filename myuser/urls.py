from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView)
from . import views


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('detail/<int:pk>/', views.UserDetailView.as_view()),
    path('update/<int:pk>/', views.UserUpdateView.as_view()),
    path('create/', views.UserCreateView.as_view()),
]
