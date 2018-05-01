from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'elections'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='elections/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='elections/logged_out.html'), name='logout'),
    path('election/<int:election_id>/', views.detail, name='detail'),
]
