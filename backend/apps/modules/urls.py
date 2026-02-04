from django.urls import path
from . import views

urlpatterns = [
    path('', views.ModuleListView.as_view(), name='module-list'),
    path('<slug:slug>/', views.ModuleDetailView.as_view(), name='module-detail'),
    path('<int:module_id>/unlock/', views.unlock_module, name='module-unlock'),
]
