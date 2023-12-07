from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('login',views.login),
    path('register',views.register),
    path('dashboard',views.dashboard),
    path('add_item_form',views.add_item_form),
    path('dashboard/filter',views.filter),
]