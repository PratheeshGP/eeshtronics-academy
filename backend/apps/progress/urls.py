from django.urls import path
from . import views

urlpatterns = [
    path('update/', views.update_mission_progress, name='progress-update'),
    path('mission/<int:mission_id>/complete/', views.complete_mission, name='mission-complete'),
    path('user/', views.user_progress_summary, name='user-progress'),
    path('achievements/', views.my_achievements, name='my-achievements'),
]
