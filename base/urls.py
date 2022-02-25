from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update-user/', views.update_user, name='update-user'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('edit-room/<str:pk>/', views.update_room, name='edit-room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),
    path('delete-comment/<str:pk>/', views.delete_comment, name='delete-comment'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('topics/', views.topics, name='topics'),
    path('activities/', views.activities, name='activities'),
    
    
]
