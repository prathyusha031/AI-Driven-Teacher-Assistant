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
    path('quiz-results/',views.quiz_results,name='quiz_results'),
    path('start-learning/',views.start_learning,name='start_learning'),
    path('logout/', views.logout_view, name='logout'),
    path('chat/',views.chat_page,name='chat'),
    path('download-summary/<int:doc_id>/',views.download_summary,name='download_summary'),
]