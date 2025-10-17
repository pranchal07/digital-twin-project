"""
Machine Learning model training for health risk prediction
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from django.conf import settings
from .etl import extract_health_data, transform_features, normalize_features

def create_synthetic_training_data(n_samples=1000):
    """
    Create synthetic training data for the health risk prediction model
    This is used when no real data is available for training
    """
    np.random.seed(42)  # For reproducibility

    data = []
    for i in range(n_samples):
        # Generate realistic health data
        heart_rate = np.random.normal(75, 15)  # Normal: 60-100
        bp_systolic = np.random.normal(120, 20)  # Normal: 90-120
        bp_diastolic = np.random.normal(80, 15)  # Normal: 60-80
        temperature = np.random.normal(98.6, 1.5)  # Normal: 98.6
        spo2 = np.random.normal(98, 3)  # Normal: 95-100

        sleep_hours = np.random.normal(7.5, 1.5)  # Normal: 7-9
        stress_level = np.random.randint(1, 11)
        diet_quality = np.random.randint(1, 11)
        water_intake = np.random.normal(8, 3)
        physical_activity = np.random.normal(1.5, 1)

        study_hours = np.random.normal(6, 2)
        attendance = np.random.normal(85, 15)
        assignments_completed = np.random.normal(80, 20)
        focus_level = np.random.randint(1, 11)

        # Ensure values are within valid ranges
        heart_rate = np.clip(heart_rate, 40, 200)
        bp_systolic = np.clip(bp_systolic, 70, 200)
        bp_diastolic = np.clip(bp_diastolic, 40, 120)
        temperature = np.clip(temperature, 95, 105)
        spo2 = np.clip(spo2, 70, 100)
        sleep_hours = np.clip(sleep_hours, 0, 24)
        water_intake = np.clip(water_intake, 0, 20)
        physical_activity = np.clip(physical_activity, 0, 10)
        study_hours = np.clip(study_hours, 0, 16)
        attendance = np.clip(attendance, 0, 100)
        assignments_completed = np.clip(assignments_completed, 0, 100)

        # Create a mock health data instance for feature transformation
        class MockHealthData:
            def __init__(self):
                self.heart_rate = heart_rate
                self.bp_systolic = bp_systolic
                self.bp_diastolic = bp_diastolic
                self.temperature = temperature
                self.spo2 = spo2
                self.sleep_hours = sleep_hours
                self.stress_level = stress_level
                self.diet_quality = diet_quality
                self.water_intake = water_intake
                self.physical_activity = physical_activity
                self.study_hours = study_hours
                self.attendance = attendance
                self.assignments_completed = assignments_completed
                self.focus_level = focus_level

        mock_data = MockHealthData()
        features, _ = transform_features(mock_data)

        # Calculate risk level based on features
        risk_score = calculate_risk_score(mock_data)

        if risk_score < 25:
            risk_level = 0  # LOW
        elif risk_score < 50:
            risk_level = 1  # MEDIUM
        elif risk_score < 75:
            risk_level = 2  # HIGH
        else:
            risk_level = 3  # CRITICAL

        data.append({
            'features': features,
            'risk_level': risk_level,
            'risk_score': risk_score
        })

    return data

def calculate_risk_score(health_data):
    """
    Calculate risk score based on health data
    """
    risk_factors = 0

    # Heart rate risk
    if health_data.heart_rate < 60 or health_data.heart_rate > 100:
        risk_factors += 10

    # Blood pressure risk
    if health_data.bp_systolic > 140 or health_data.bp_diastolic > 90:
        risk_factors += 20
    elif health_data.bp_systolic < 90 or health_data.bp_diastolic < 60:
        risk_factors += 10

    # Temperature risk
    if health_data.temperature < 97 or health_data.temperature > 100:
        risk_factors += 15

    # Oxygen saturation risk
    if health_data.spo2 < 95:
        risk_factors += 25

    # Sleep risk
    if health_data.sleep_hours < 6 or health_data.sleep_hours > 10:
        risk_factors += 10

    # Stress risk
    if health_data.stress_level > 7:
        risk_factors += 15

    # Diet risk
    if health_data.diet_quality < 5:
        risk_factors += 10

    # Hydration risk
    if health_data.water_intake < 6:
        risk_factors += 5

    # Activity risk
    if health_data.physical_activity < 0.5:
        risk_factors += 10

    # Academic stress risk
    if health_data.focus_level < 4 or health_data.study_hours > 12:
        risk_factors += 10

    return min(risk_factors, 100)  # Cap at 100

def train_model():
    """
    Train the health risk prediction model
    """
    print("Generating synthetic training data...")
    training_data = create_synthetic_training_data(1000)

    # Prepare features and labels
    X = []
    y = []

    for sample in training_data:
        features = normalize_features(sample['features'])
        X.append(features)
        y.append(sample['risk_level'])

    X = np.array(X)
    y = np.array(y)

    print(f"Training with {len(X)} samples, {X.shape[1]} features")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )

    print("Training model...")
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Model accuracy: {accuracy:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, 
                              target_names=['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']))

    # Save model
    model_dir = os.path.join(settings.BASE_DIR, 'twin_app', 'ml', 'models')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'health_risk_model.joblib')

    joblib.dump(model, model_path)
    print(f"Model saved to: {model_path}")

    return model

if __name__ == "__main__":
    train_model()
