"""
ETL (Extract, Transform, Load) module for health data processing
"""
import numpy as np
import pandas as pd
from django.db.models import Q
from ..models import HealthData

def extract_health_data(user=None, days=30):
    """
    Extract health data from database
    """
    queryset = HealthData.objects.all()

    if user:
        queryset = queryset.filter(user=user)

    # Convert to pandas DataFrame
    data = []
    for entry in queryset:
        data.append({
            'user_id': entry.user.id,
            'heart_rate': entry.heart_rate,
            'bp_systolic': entry.bp_systolic,
            'bp_diastolic': entry.bp_diastolic,
            'temperature': entry.temperature,
            'spo2': entry.spo2,
            'sleep_hours': entry.sleep_hours,
            'stress_level': entry.stress_level,
            'diet_quality': entry.diet_quality,
            'water_intake': entry.water_intake,
            'physical_activity': entry.physical_activity,
            'study_hours': entry.study_hours,
            'attendance': entry.attendance,
            'assignments_completed': entry.assignments_completed,
            'focus_level': entry.focus_level,
            'health_score': entry.health_score,
            'timestamp': entry.timestamp
        })

    df = pd.DataFrame(data)
    return df

def transform_features(health_data_instance):
    """
    Transform raw health data into ML features
    """
    # Extract features from health data
    features = {
        'heart_rate': health_data_instance.heart_rate,
        'bp_systolic': health_data_instance.bp_systolic,
        'bp_diastolic': health_data_instance.bp_diastolic,
        'temperature': health_data_instance.temperature,
        'spo2': health_data_instance.spo2,
        'sleep_hours': health_data_instance.sleep_hours,
        'stress_level': health_data_instance.stress_level,
        'diet_quality': health_data_instance.diet_quality,
        'water_intake': health_data_instance.water_intake,
        'physical_activity': health_data_instance.physical_activity,
        'study_hours': health_data_instance.study_hours,
        'attendance': health_data_instance.attendance,
        'assignments_completed': health_data_instance.assignments_completed,
        'focus_level': health_data_instance.focus_level,
    }

    # Derived features
    features['bp_mean'] = (features['bp_systolic'] + features['bp_diastolic']) / 2
    features['bp_pulse_pressure'] = features['bp_systolic'] - features['bp_diastolic']
    features['sleep_deficit'] = max(0, 8 - features['sleep_hours'])  # 8 hours is optimal
    features['activity_to_sleep_ratio'] = features['physical_activity'] / max(features['sleep_hours'], 1)
    features['stress_to_focus_ratio'] = features['stress_level'] / max(features['focus_level'], 1)
    features['academic_performance'] = (features['attendance'] + features['assignments_completed']) / 2

    # Normalize temperature (convert to deviation from normal)
    features['temp_deviation'] = abs(features['temperature'] - 98.6)

    # Create feature vector for ML model
    feature_vector = np.array([
        features['heart_rate'],
        features['bp_systolic'],
        features['bp_diastolic'],
        features['temperature'],
        features['spo2'],
        features['sleep_hours'],
        features['stress_level'],
        features['diet_quality'],
        features['water_intake'],
        features['physical_activity'],
        features['study_hours'],
        features['attendance'],
        features['assignments_completed'],
        features['focus_level'],
        features['bp_mean'],
        features['bp_pulse_pressure'],
        features['sleep_deficit'],
        features['activity_to_sleep_ratio'],
        features['stress_to_focus_ratio'],
        features['academic_performance'],
        features['temp_deviation']
    ])

    return feature_vector, features

def normalize_features(feature_vector):
    """
    Normalize features to 0-1 range for better ML performance
    """
    # Define expected ranges for normalization
    ranges = {
        0: (40, 200),    # heart_rate
        1: (70, 200),    # bp_systolic
        2: (40, 120),    # bp_diastolic
        3: (95, 105),    # temperature
        4: (70, 100),    # spo2
        5: (0, 24),      # sleep_hours
        6: (1, 10),      # stress_level
        7: (1, 10),      # diet_quality
        8: (0, 20),      # water_intake
        9: (0, 10),      # physical_activity
        10: (0, 16),     # study_hours
        11: (0, 100),    # attendance
        12: (0, 100),    # assignments_completed
        13: (1, 10),     # focus_level
        14: (55, 160),   # bp_mean
        15: (20, 80),    # bp_pulse_pressure
        16: (0, 8),      # sleep_deficit
        17: (0, 5),      # activity_to_sleep_ratio
        18: (0.1, 10),   # stress_to_focus_ratio
        19: (0, 100),    # academic_performance
        20: (0, 10),     # temp_deviation
    }

    normalized = np.zeros_like(feature_vector)
    for i, value in enumerate(feature_vector):
        min_val, max_val = ranges.get(i, (0, 1))
        normalized[i] = (value - min_val) / (max_val - min_val)
        normalized[i] = np.clip(normalized[i], 0, 1)  # Ensure 0-1 range

    return normalized
