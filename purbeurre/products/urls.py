from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('search/', views.ProductsView.as_view(), name="search"),
    path('product/', views.ProductView.as_view(), name="product"),
    path('save/', views.SaveView.as_view(), name="save"),
    path('delete/', views.DeleteView.as_view(), name="delete"),
    path('my_products/', views.MyProductsView.as_view(), name="my_products"),
]
