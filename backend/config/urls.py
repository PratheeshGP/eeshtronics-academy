"""
URL Configuration for EngineerLab Backend
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('apps.users.urls')),
    path('api/paths/', include('apps.paths.urls')),
    path('api/modules/', include('apps.modules.urls')),
    path('api/missions/', include('apps.missions.urls')),
    path('api/labs/', include('apps.labs.urls')),
    path('api/progress/', include('apps.progress.urls')),
    path('api/ether/', include('apps.economy.urls')),
    
    # JWT token refresh
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
