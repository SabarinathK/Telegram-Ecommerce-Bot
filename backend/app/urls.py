from .views import ProductView
from django.urls import path

urlpatterns = [
    path('products/', ProductView.as_view(), name='product-list'),
]