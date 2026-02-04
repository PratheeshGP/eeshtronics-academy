from django.urls import path
from . import views

urlpatterns = [
    path('', views.PathListView.as_view(), name='path-list'),
    path('<slug:slug>/', views.PathDetailView.as_view(), name='path-detail'),
    path('<int:path_id>/enroll/', views.enroll_in_path, name='path-enroll'),
    path('enrollments/', views.my_enrollments, name='my-enrollments'),
]
