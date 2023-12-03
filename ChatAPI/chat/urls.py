from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_convo, name='start_convo'),
    path('<int:convo_id>/', views.get_conversation, name='get_conversation'),
    path('', views.conversations, name='conversations'),
    path('create_room/', views.create_room, name='create_room'),
    path('get_room/<int:room_id>/', views.get_room, name='get_room'),
    path('join_room/<int:room_id>/', views.join_room, name='join_room'),
    path('leave_room/<int:room_id>/', views.leave_room, name='leave_room'),
]