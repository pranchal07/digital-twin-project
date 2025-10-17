"""
Health risk prediction module
"""
import numpy as np
import joblib
import os
from django.conf import settings
from .etl import transform_features, normalize_features
from .model_train import train_model, calculate_risk_score

def get_model():
    """
    Load the trained model or train a new one if not exists
    """
    model_path = os.path.join(settings.BASE_DIR, 'twin_app', 'ml', 'models', 'health_risk_model.joblib')

    try:
        model = joblib.load(model_path)
        return model
    except (FileNotFoundError, Exception):
        # Train new model if not found
        print("Model not found. Training new model...")
        model = train_model()
        return model

def get_risk_prediction(health_data):
    """
    Generate risk prediction for health data

    Args:
        health_data: HealthData instance

    Returns:
        dict: {
            'risk_score': float,
            'risk_level': str,
            'recommendations': str,
            'confidence': float
        }
    """
    try:
        # Transform features
        features, feature_dict = transform_features(health_data)
        normalized_features = normalize_features(features)

        # Load model and predict
        model = get_model()

        # Predict risk level and probabilities
        risk_level_pred = model.predict([normalized_features])[0]
        risk_probabilities = model.predict_proba([normalized_features])[0]

        # Map risk levels
        risk_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        predicted_risk_level = risk_levels[risk_level_pred]

        # Calculate risk score (0-100)
        risk_score = calculate_risk_score(health_data)

        # Get confidence (highest probability)
        confidence = max(risk_probabilities)

        # Generate recommendations
        recommendations = generate_recommendations(health_data, feature_dict)

        return {
            'risk_score': risk_score,
            'risk_level': predicted_risk_level,
            'recommendations': recommendations,
            'confidence': confidence
        }

    except Exception as e:
        # Fallback prediction
        risk_score = calculate_risk_score(health_data)

        if risk_score < 25:
            risk_level = 'LOW'
        elif risk_score < 50:
            risk_level = 'MEDIUM'
        elif risk_score < 75:
            risk_level = 'HIGH'
        else:
            risk_level = 'CRITICAL'

        recommendations = generate_recommendations(health_data, {})

        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'recommendations': recommendations,
            'confidence': 0.5
        }

def generate_recommendations(health_data, feature_dict):
    """
    Generate personalized health recommendations
    """
    recommendations = []

    # Heart rate recommendations
    if health_data.heart_rate < 60:
        recommendations.append("Consider increasing physical activity to improve heart rate.")
    elif health_data.heart_rate > 100:
        recommendations.append("High heart rate detected. Consider stress management and consult a healthcare provider.")

    # Blood pressure recommendations
    if health_data.bp_systolic > 140 or health_data.bp_diastolic > 90:
        recommendations.append("High blood pressure detected. Reduce sodium intake and consider medical consultation.")

    # Temperature recommendations
    if health_data.temperature < 97:
        recommendations.append("Low body temperature. Ensure adequate clothing and warm environment.")
    elif health_data.temperature > 100:
        recommendations.append("Elevated temperature detected. Monitor for fever and stay hydrated.")

    # Oxygen saturation recommendations
    if health_data.spo2 < 95:
        recommendations.append("Low oxygen saturation. Seek immediate medical attention if persistent.")

    # Sleep recommendations
    if health_data.sleep_hours < 7:
        recommendations.append("Insufficient sleep detected. Aim for 7-9 hours of quality sleep nightly.")
    elif health_data.sleep_hours > 9:
        recommendations.append("Excessive sleep may indicate underlying issues. Maintain consistent sleep schedule.")

    # Stress recommendations
    if health_data.stress_level > 7:
        recommendations.append("High stress levels detected. Practice meditation, deep breathing, or yoga.")

    # Diet recommendations
    if health_data.diet_quality < 5:
        recommendations.append("Poor diet quality. Include more fruits, vegetables, and whole grains in your meals.")

    # Hydration recommendations
    if health_data.water_intake < 6:
        recommendations.append("Insufficient hydration. Aim for 8 glasses of water daily.")

    # Physical activity recommendations
    if health_data.physical_activity < 1:
        recommendations.append("Low physical activity. Include at least 30 minutes of exercise daily.")

    # Academic stress recommendations
    if health_data.study_hours > 10:
        recommendations.append("Excessive study hours detected. Take regular breaks and practice time management.")

    if health_data.focus_level < 5:
        recommendations.append("Low focus levels. Ensure adequate sleep, nutrition, and consider study environment improvements.")

    # Academic performance recommendations
    if health_data.attendance < 80:
        recommendations.append("Low attendance may affect academic performance. Prioritize consistent class participation.")

    if health_data.assignments_completed < 70:
        recommendations.append("Low assignment completion rate. Improve time management and seek academic support if needed.")

    # General wellness recommendations
    if not recommendations:
        recommendations.append("Great job! Your health metrics look good. Continue maintaining healthy habits.")
    else:
        # Add general wellness advice
        recommendations.append("Remember to maintain a balanced lifestyle with proper nutrition, exercise, and rest.")

    return " ".join(recommendations)

def get_feature_importance(health_data):
    """
    Get feature importance for the prediction
    """
    try:
        model = get_model()
        feature_names = [
            'heart_rate', 'bp_systolic', 'bp_diastolic', 'temperature', 'spo2',
            'sleep_hours', 'stress_level', 'diet_quality', 'water_intake', 'physical_activity',
            'study_hours', 'attendance', 'assignments_completed', 'focus_level',
            'bp_mean', 'bp_pulse_pressure', 'sleep_deficit', 'activity_to_sleep_ratio',
            'stress_to_focus_ratio', 'academic_performance', 'temp_deviation'
        ]

        importance_scores = model.feature_importances_

        feature_importance = []
        for i, (name, score) in enumerate(zip(feature_names, importance_scores)):
            feature_importance.append({
                'feature': name,
                'importance': score,
                'rank': i + 1
            })

        # Sort by importance
        feature_importance.sort(key=lambda x: x['importance'], reverse=True)

        return feature_importance

    except Exception:
        return []
