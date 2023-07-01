from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_page),
    path('api/list/get', views.get_url, name='get_url'),
    path('list/', views.list_page),
    path('list/<str:list_id>', views.list_page),
    path('random/', views.random_page),
    path('random/<str:list_id>', views.random_page),
]