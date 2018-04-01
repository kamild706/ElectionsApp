from django.urls import path, include
import django.contrib.auth.urls

from . import views

app_name = 'elections'
urlpatterns = [
    # path('test/', views.index),
    path('', views.IndexView.as_view(), name='index'),
]
