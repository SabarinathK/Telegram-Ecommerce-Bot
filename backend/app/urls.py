from .views import ProductView
from django.urls import path
from .views import TelegramWebhookView,SetWebhookView

urlpatterns = [
    path('products/', ProductView.as_view(), name='product-list'),
    path('webhook/<str:token>/', TelegramWebhookView.as_view(), name="telegram_webhook"),
    path("set-webhook/", SetWebhookView.as_view(), name="set_webhook"),
]