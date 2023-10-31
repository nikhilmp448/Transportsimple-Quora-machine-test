from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('', views.home, name='home'),
    path('question/', views.create_question, name='create_question'),
    path('my-question/', views.my_question, name='my_question'),
    path('answers/<int:question_id>/', views.view_all_answer, name='view_all_answer'),
    path('answer/<int:question_id>/', views.answer_question, name='answer_question'),
    path('like/<int:answer_id>/', views.like_answer, name='like_answer'),
]