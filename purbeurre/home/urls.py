from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('legal_notice', views.legal_notice, name="legal_notice"),
]
