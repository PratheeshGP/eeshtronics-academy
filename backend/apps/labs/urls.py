from django.urls import path
from . import views

urlpatterns = [
    path('', views.LabListView.as_view(), name='lab-list'),
    path('<int:pk>/', views.LabDetailView.as_view(), name='lab-detail'),
    path('start/', views.start_lab, name='lab-start'),
    path('<int:session_id>/stop/', views.stop_lab, name='lab-stop'),
    path('<int:session_id>/status/', views.lab_status, name='lab-status'),
    path('sessions/', views.my_sessions, name='my-sessions'),
]
