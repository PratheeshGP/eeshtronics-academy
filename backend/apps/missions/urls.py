from django.urls import path
from . import views

urlpatterns = [
    path('', views.MissionListView.as_view(), name='mission-list'),
    path('<slug:slug>/', views.MissionDetailView.as_view(), name='mission-detail'),
    path('artifacts/', views.ArtifactListView.as_view(), name='artifact-list'),
    path('artifacts/submit/', views.ArtifactCreateView.as_view(), name='artifact-submit'),
]
