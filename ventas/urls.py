from django.urls import path
from .views import *

app_name = 'ventas'

urlpatterns = [
    path('', index, name="index"),
]
