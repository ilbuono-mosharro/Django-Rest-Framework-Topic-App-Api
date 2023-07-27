from django.urls import path
from rest_framework.authtoken import views as rest_views
from . import views

app_name = "api_accounts"

urlpatterns = [
    path("accounts/sign-up/", views.SignUp.as_view(), name="sign-up"),
    path('accounts/api-token-auth/', rest_views.obtain_auth_token),
    path('accounts/profile/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='profile'),
    path('accounts/logout/', views.LogoutView.as_view(), name="logout"),
]
