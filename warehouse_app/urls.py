from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('login',views.login),
    path('register',views.register),
    path('dashboard',views.dashboard),
    path('add_item_form',views.add_item_form),
    path('dashboard/filter',views.filter),
    path('item_view/<id>',views.item_view),
    path('item_view/delete_category/<category_id>/<item_id>',views.delete_category_item),
    path('item_view/add_category/<id>',views.add_category),
    path('item_view/edit_form/<id>',views.item_edit_form),
    path('edit_item/<id>',views.edit_item),
    path('dashboard/categories',views.categories),
    path('category/add_item',views.add_item_category),
    path('category/creat_category',views.create_category),
    path('category/delete_category/<id>',views.delete_category),
    path('create_shipment_form',views.create_shipment_form),
]