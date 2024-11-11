from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name='logout'),
    path('update_info/<str:username>/', views.update_info),
    path('time-keeping/', views.time_keeping, name='time-keeping'),
    path('sheet/<str:username>/', views.sheet, name='sheet'),
    path('profile/<str:username>/', views.profile_detail, name='profile-detail'),
    path('letters/', views.letters, name='letters'),
    path('letters/<int:idletter>/', views.letter_detail, name='letter-detail')
]