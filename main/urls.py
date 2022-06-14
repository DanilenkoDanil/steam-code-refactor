from django.urls import path
from . import views
from .views import DynamicCodeLoad, DynamicAccountLoad


urlpatterns = [
    path('', views.head),
    path('account/', views.index),
    path('get_code/', DynamicCodeLoad.as_view(), name='load_code'),
    path('get_account/', DynamicAccountLoad.as_view(), name='load_account')
]
