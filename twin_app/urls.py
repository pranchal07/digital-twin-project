from django.urls import path
from . import views

app_name = 'twin_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('manual-entry/', views.manual_entry, name='manual_entry'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('analytics/', views.analytics, name='analytics'),
    path('about/', views.about, name='about'),
    path('api/health-data/', views.get_health_data_json, name='health_data_json'),
    path('api/predictions/', views.get_predictions_json, name='predictions_json'),
]
