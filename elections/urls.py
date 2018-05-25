from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'elections'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='elections/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='elections/logged_out.html'), name='logout'),
    path('election/<int:election_id>/', views.election_detail, name='electionDetail'),
    path('questionnaire/<int:election_id>/', views.questionnaire_detail, name='questionnaireDetail'),
]
