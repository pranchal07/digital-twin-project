from django.contrib import admin
from .models import HealthData, UserProfile, Prediction

@admin.register(HealthData)
class HealthDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'heart_rate', 'sleep_hours', 'stress_level', 'study_hours')
    list_filter = ('timestamp', 'stress_level')
    search_fields = ('user__username',)
    date_hierarchy = 'timestamp'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'height', 'weight', 'created_at')
    search_fields = ('user__username', 'user__email')

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('health_data', 'risk_score', 'risk_level', 'created_at')
    list_filter = ('risk_level', 'created_at')
    search_fields = ('health_data__user__username',)
