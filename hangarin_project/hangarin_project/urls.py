from django.contrib import admin
from django.urls import path, include
from hangarin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')),  # Added PWA route
    path('accounts/', include('allauth.urls')),  # Handles login, logout, signup & OAuth
    path('', views.task_board, name='task_board'),
]