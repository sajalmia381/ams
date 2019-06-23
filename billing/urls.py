from django.urls import path
from .views import card_method_view, card_method_view_api

app_name = 'billing'
urlpatterns = [
    path('billing/card-method/', card_method_view, name='card_method'),
    path('billing/card-method/create/', card_method_view_api, name='card_method_endpoint')
]