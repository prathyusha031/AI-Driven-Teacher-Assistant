from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_document, name='upload'),
    path('quiz/', views.quiz_page, name='quiz'),
    path('summary/', views.summary_page, name='summary'),
    path('profile/', views.profile_page, name='profile'),
]