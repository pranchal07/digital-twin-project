from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import HealthData, UserProfile, Prediction
from .forms import HealthDataForm, UserProfileForm
from .ml.model_predict import get_risk_prediction

def index(request):
    """Home page view"""
    context = {
        'total_users': User.objects.count(),
        'total_entries': HealthData.objects.count(),
        'avg_health_score': HealthData.objects.aggregate(
            avg_score=Avg('heart_rate')  # Placeholder calculation
        )['avg_score'] or 0,
    }
    return render(request, 'twin_app/index.html', context)

def manual_entry(request):
    """Manual data entry view"""
    # Create anonymous user if not exists
    user, created = User.objects.get_or_create(
        username='anonymous_user',
        defaults={
            'first_name': 'Anonymous',
            'last_name': 'User',
            'email': 'anonymous@example.com'
        }
    )

    if request.method == 'POST':
        form = HealthDataForm(request.POST)
        if form.is_valid():
            health_data = form.save(commit=False)
            health_data.user = user
            health_data.save()

            # Generate prediction
            try:
                prediction_result = get_risk_prediction(health_data)
                Prediction.objects.create(
                    health_data=health_data,
                    risk_score=prediction_result['risk_score'],
                    risk_level=prediction_result['risk_level'],
                    recommendations=prediction_result['recommendations'],
                    confidence=prediction_result['confidence']
                )
            except Exception as e:
                messages.warning(request, f'Data saved but prediction failed: {str(e)}')

            messages.success(request, 'Health data submitted successfully!')
            return redirect('twin_app:dashboard')
    else:
        form = HealthDataForm()

    return render(request, 'twin_app/manual_entry.html', {'form': form})

def dashboard(request):
    """Dashboard view with health analytics"""
    # Get anonymous user data
    try:
        user = User.objects.get(username='anonymous_user')

        # Get latest health data
        latest_health_data = HealthData.objects.filter(user=user).first()

        # Get recent entries (last 7 days)
        week_ago = timezone.now() - timedelta(days=7)
        recent_entries = HealthData.objects.filter(
            user=user, 
            timestamp__gte=week_ago
        ).order_by('-timestamp')

        # Calculate averages
        avg_data = recent_entries.aggregate(
            avg_heart_rate=Avg('heart_rate'),
            avg_sleep_hours=Avg('sleep_hours'),
            avg_stress_level=Avg('stress_level'),
            avg_study_hours=Avg('study_hours')
        )

        # Get latest prediction
        latest_prediction = None
        if latest_health_data:
            try:
                latest_prediction = latest_health_data.prediction
            except Prediction.DoesNotExist:
                pass

        context = {
            'latest_health_data': latest_health_data,
            'recent_entries': recent_entries,
            'avg_data': avg_data,
            'latest_prediction': latest_prediction,
            'health_score': latest_health_data.health_score if latest_health_data else 0,
            'total_entries': HealthData.objects.filter(user=user).count(),
        }

    except User.DoesNotExist:
        context = {
            'no_data': True,
            'message': 'No health data found. Please submit data using the manual entry form.'
        }

    return render(request, 'twin_app/dashboard.html', context)

def profile(request):
    """User profile view"""
    try:
        user = User.objects.get(username='anonymous_user')
        profile, created = UserProfile.objects.get_or_create(user=user)

        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('twin_app:profile')
        else:
            form = UserProfileForm(instance=profile)

        # Get user stats
        health_data_count = HealthData.objects.filter(user=user).count()
        avg_health_score = 0
        if health_data_count > 0:
            latest_entry = HealthData.objects.filter(user=user).first()
            avg_health_score = latest_entry.health_score if latest_entry else 0

        context = {
            'form': form,
            'profile': profile,
            'health_data_count': health_data_count,
            'avg_health_score': avg_health_score,
        }

    except User.DoesNotExist:
        context = {
            'no_user': True,
            'message': 'Please submit health data first to create a profile.'
        }

    return render(request, 'twin_app/profile.html', context)

def analytics(request):
    """Analytics view with detailed charts"""
    try:
        user = User.objects.get(username='anonymous_user')

        # Get last 30 days of data
        month_ago = timezone.now() - timedelta(days=30)
        health_data = HealthData.objects.filter(
            user=user,
            timestamp__gte=month_ago
        ).order_by('timestamp')

        # Prepare data for charts
        chart_data = {
            'dates': [entry.timestamp.strftime('%Y-%m-%d') for entry in health_data],
            'heart_rate': [entry.heart_rate for entry in health_data],
            'sleep_hours': [entry.sleep_hours for entry in health_data],
            'stress_level': [entry.stress_level for entry in health_data],
            'study_hours': [entry.study_hours for entry in health_data],
            'health_scores': [entry.health_score for entry in health_data],
        }

        # Calculate statistics
        stats = {
            'total_entries': health_data.count(),
            'avg_health_score': sum(chart_data['health_scores']) / len(chart_data['health_scores']) if chart_data['health_scores'] else 0,
            'last_entry': health_data.last().timestamp if health_data.exists() else None,
            'data_streak': health_data.count(),  # Simplified streak calculation
        }

        context = {
            'chart_data': chart_data,
            'stats': stats,
            'has_data': health_data.exists(),
        }

    except User.DoesNotExist:
        context = {
            'has_data': False,
            'message': 'No health data found. Please submit data using the manual entry form.'
        }

    return render(request, 'twin_app/analytics.html', context)

def about(request):
    """About page view"""
    return render(request, 'twin_app/about.html')

def get_health_data_json(request):
    """API endpoint for health data (for AJAX requests)"""
    try:
        user = User.objects.get(username='anonymous_user')
        health_data = HealthData.objects.filter(user=user).order_by('-timestamp')[:30]

        data = []
        for entry in health_data:
            data.append({
                'timestamp': entry.timestamp.isoformat(),
                'heart_rate': entry.heart_rate,
                'sleep_hours': entry.sleep_hours,
                'stress_level': entry.stress_level,
                'study_hours': entry.study_hours,
                'health_score': entry.health_score,
            })

        return JsonResponse({'data': data})

    except User.DoesNotExist:
        return JsonResponse({'error': 'No user data found'}, status=404)

def get_predictions_json(request):
    """API endpoint for predictions data"""
    try:
        user = User.objects.get(username='anonymous_user')
        predictions = Prediction.objects.filter(
            health_data__user=user
        ).order_by('-created_at')[:10]

        data = []
        for pred in predictions:
            data.append({
                'timestamp': pred.created_at.isoformat(),
                'risk_score': pred.risk_score,
                'risk_level': pred.risk_level,
                'recommendations': pred.recommendations,
                'confidence': pred.confidence,
            })

        return JsonResponse({'data': data})

    except User.DoesNotExist:
        return JsonResponse({'error': 'No user data found'}, status=404)
