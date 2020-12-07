from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.user_account, name="user_account"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout_user"),
    path('new/', views.new_account, name="new_account"),
    path('create_new/', views.create_new, name="create_new"),
    path('check_user_login/', views.check_user_login, name="check_user_login"),
    path('check_email/', views.check_email, name="check_email"),
    path('check_pwd/', views.check_pwd, name="check_pwd"),
]
