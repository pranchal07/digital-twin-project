from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)], null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_data')
    timestamp = models.DateTimeField(default=timezone.now)

    # Vital Signs
    heart_rate = models.IntegerField(
        validators=[MinValueValidator(40), MaxValueValidator(200)],
        help_text="Heart rate in beats per minute"
    )
    bp_systolic = models.IntegerField(
        validators=[MinValueValidator(70), MaxValueValidator(200)],
        help_text="Systolic blood pressure in mmHg"
    )
    bp_diastolic = models.IntegerField(
        validators=[MinValueValidator(40), MaxValueValidator(120)],
        help_text="Diastolic blood pressure in mmHg"
    )
    temperature = models.FloatField(
        validators=[MinValueValidator(95.0), MaxValueValidator(105.0)],
        help_text="Body temperature in Fahrenheit"
    )
    spo2 = models.IntegerField(
        validators=[MinValueValidator(70), MaxValueValidator(100)],
        help_text="Blood oxygen saturation percentage"
    )

    # Lifestyle Factors
    sleep_hours = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        help_text="Hours of sleep"
    )
    stress_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Stress level from 1-10"
    )
    diet_quality = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Diet quality from 1-10"
    )
    water_intake = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text="Glasses of water consumed"
    )
    physical_activity = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Hours of physical activity"
    )

    # Academic Performance
    study_hours = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(16)],
        help_text="Hours of study per day"
    )
    attendance = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Class attendance percentage"
    )
    assignments_completed = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Assignments completion percentage"
    )
    focus_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Focus level from 1-10"
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Health Data"

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    @property
    def health_score(self):
        """Calculate a simple health score based on various metrics"""
        # Normalize all values to 0-100 scale
        hr_score = max(0, 100 - abs(self.heart_rate - 70))  # Optimal around 70
        bp_score = max(0, 100 - abs((self.bp_systolic + self.bp_diastolic) - 180))  # Optimal around 120/80
        temp_score = max(0, 100 - abs(self.temperature - 98.6) * 10)  # Optimal at 98.6
        spo2_score = self.spo2  # Already 0-100

        sleep_score = min(100, max(0, (self.sleep_hours - 4) * 20))  # 4-9 hours range
        stress_score = (11 - self.stress_level) * 10  # Lower stress is better
        diet_score = self.diet_quality * 10
        water_score = min(100, self.water_intake * 12.5)  # 8 glasses = 100
        activity_score = min(100, self.physical_activity * 50)  # 2 hours = 100

        study_score = min(100, self.study_hours * 12.5)  # 8 hours = 100
        attendance_score = self.attendance
        assignments_score = self.assignments_completed
        focus_score = self.focus_level * 10

        # Weighted average
        total_score = (
            hr_score * 0.08 + bp_score * 0.08 + temp_score * 0.05 + spo2_score * 0.08 +
            sleep_score * 0.12 + stress_score * 0.10 + diet_score * 0.10 + 
            water_score * 0.05 + activity_score * 0.10 +
            study_score * 0.08 + attendance_score * 0.08 + 
            assignments_score * 0.04 + focus_score * 0.04
        )

        return round(total_score, 1)

class Prediction(models.Model):
    RISK_LEVELS = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
        ('CRITICAL', 'Critical Risk'),
    ]

    health_data = models.OneToOneField(HealthData, on_delete=models.CASCADE, related_name='prediction')
    risk_score = models.FloatField(help_text="Risk score from 0-100")
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS)
    recommendations = models.TextField(help_text="AI-generated recommendations")
    confidence = models.FloatField(help_text="Model confidence (0-1)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.health_data.user.username} - {self.risk_level}"
