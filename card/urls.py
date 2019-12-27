from django.urls import path
from . import views


app_name = 'cards'

urlpatterns = [
    path('', views.card_list, name='card_list'),
]
