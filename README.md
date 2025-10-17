# Digital Twin of the Human Body — Student Edition Framework (Django Backend)

A comprehensive Django-based backend for the Digital Twin Student Health Framework that provides health monitoring, predictive analytics, and academic performance correlation through a robust web API and interface.

## 🎯 Project Overview

This Django backend powers the Digital Twin Student Health Framework, providing:

- **Health Data Management**: Comprehensive storage and retrieval of student health metrics
- **AI-Powered Predictions**: Machine learning models for health risk assessment
- **Analytics Engine**: Advanced data processing and trend analysis
- **User Management**: Student profile and goal tracking
- **API Endpoints**: RESTful APIs for frontend integration

## ✨ Features

### 🏥 Health Data Models
- **Vital Signs**: Heart rate, blood pressure, temperature, oxygen saturation
- **Lifestyle Metrics**: Sleep patterns, stress levels, diet quality, physical activity
- **Academic Data**: Study hours, attendance, focus levels, assignment completion
- **Predictions**: AI-generated health risk assessments and recommendations

### 🤖 Machine Learning Pipeline
- **Data ETL**: Extract, Transform, Load operations for health data
- **Model Training**: Automated training pipeline with synthetic data generation
- **Risk Prediction**: Real-time health risk assessment
- **Recommendation Engine**: Personalized health and academic recommendations

### 📊 Analytics & Insights
- **Trend Analysis**: Historical data pattern recognition
- **Correlation Analysis**: Health-academic performance relationships
- **Risk Assessment**: Multi-factor health risk scoring
- **Progress Tracking**: Goal monitoring and achievement tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. **Extract the project files**
   ```bash
   unzip digital_twin_project.zip
   cd digital_twin_project
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Train the ML model (optional)**
   ```bash
   python manage.py train_model
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/
   - Manual data entry: http://127.0.0.1:8000/manual-entry/
   - Dashboard: http://127.0.0.1:8000/dashboard/

## 🗂️ Project Structure

```
digital_twin_project/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── digital_twin/               # Django project settings
│   ├── settings.py             # Configuration settings
│   ├── urls.py                 # Main URL routing
│   └── wsgi.py                 # WSGI configuration
├── twin_app/                   # Main Django application
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── urls.py                 # App URL routing
│   ├── forms.py                # Django forms
│   ├── admin.py                # Admin interface configuration
│   ├── ml/                     # Machine Learning module
│   │   ├── etl.py              # Data processing
│   │   ├── model_train.py      # Model training
│   │   ├── model_predict.py    # Prediction engine
│   │   └── models/             # Trained ML models
│   ├── templates/twin_app/     # Django templates
│   │   ├── index.html          # Homepage
│   │   ├── manual_entry.html   # Data entry form
│   │   ├── dashboard.html      # Health dashboard
│   │   ├── profile.html        # User profile
│   │   ├── analytics.html      # Analytics page
│   │   └── about.html          # About page
│   ├── management/commands/    # Custom management commands
│   │   └── train_model.py      # ML model training command
│   └── migrations/             # Database migrations
└── README.md                   # This documentation
```

## 🔧 Configuration

### Database Configuration
By default, the project uses SQLite for local development. To use PostgreSQL:

1. Install PostgreSQL adapter:
   ```bash
   pip install psycopg2
   ```

2. Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'digital_twin_db',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### Machine Learning Model
The ML model is automatically trained with synthetic data if no real data is available. To retrain:

```bash
python manage.py train_model
```

## 📚 API Endpoints

### Health Data API
- `GET /api/health-data/` - Retrieve health data in JSON format
- `GET /api/predictions/` - Get prediction results

### Web Interface
- `/` - Homepage with project overview
- `/manual-entry/` - Health data entry form
- `/dashboard/` - Health analytics dashboard
- `/profile/` - User profile management
- `/analytics/` - Advanced analytics and insights
- `/about/` - Project information

## 🏥 Health Data Model

The `HealthData` model captures comprehensive student health metrics:

### Vital Signs
- Heart Rate (40-200 bpm)
- Blood Pressure - Systolic (70-200 mmHg)
- Blood Pressure - Diastolic (40-120 mmHg)
- Body Temperature (95-105°F)
- Blood Oxygen Saturation (70-100%)

### Lifestyle Factors
- Sleep Hours (0-24 hours)
- Stress Level (1-10 scale)
- Diet Quality (1-10 scale)
- Water Intake (glasses per day)
- Physical Activity (hours per day)

### Academic Performance
- Study Hours (0-16 hours per day)
- Class Attendance (0-100%)
- Assignment Completion (0-100%)
- Focus Level (1-10 scale)

## 🤖 Machine Learning Features

### Health Risk Prediction
The system uses a Random Forest classifier to predict health risk levels:

- **LOW**: Risk score 0-24
- **MEDIUM**: Risk score 25-49
- **HIGH**: Risk score 50-74
- **CRITICAL**: Risk score 75-100

### Feature Engineering
Advanced feature engineering includes:
- Blood pressure mean and pulse pressure
- Sleep deficit calculation
- Activity-to-sleep ratios
- Stress-to-focus correlations
- Academic performance indices

### Recommendation Engine
AI-generated recommendations based on:
- Health metric deviations from normal ranges
- Academic performance indicators
- Lifestyle factor analysis
- Trend analysis and pattern recognition

## 🔒 Security & Privacy

### Data Protection
- All health data is stored locally
- No external data transmission
- SQLite encryption support
- User consent and privacy controls

### Authentication
- Django's built-in authentication system
- Session-based security
- CSRF protection
- SQL injection prevention

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

For specific app testing:
```bash
python manage.py test twin_app
```

## 🚀 Deployment

### Development
```bash
python manage.py runserver
```

### Production Considerations
1. Set `DEBUG = False` in `settings.py`
2. Configure secure `SECRET_KEY`
3. Set up proper `ALLOWED_HOSTS`
4. Use production database (PostgreSQL)
5. Configure static file serving
6. Set up HTTPS/SSL

### Environment Variables
Create a `.env` file for sensitive settings:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=your-database-url
```

## 📊 Data Analytics

### Health Score Calculation
The system calculates a comprehensive health score (0-100) based on:
- Vital signs normality (30% weight)
- Lifestyle factors (40% weight)
- Academic performance (30% weight)

### Trend Analysis
- Historical data visualization
- Pattern recognition algorithms
- Correlation analysis between health and academic metrics
- Predictive modeling for future health outcomes

## 🛠️ Development

### Adding New Features
1. Create new models in `models.py`
2. Update forms in `forms.py`
3. Add views in `views.py`
4. Update URL routing in `urls.py`
5. Create/update templates
6. Run migrations

### Custom Management Commands
Add custom commands in `twin_app/management/commands/`:
```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Description of your command'

    def handle(self, *args, **options):
        # Command logic here
        pass
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Write comprehensive tests

## 📞 Support

### Common Issues
1. **Model training fails**: Ensure all dependencies are installed
2. **Database errors**: Run `python manage.py migrate`
3. **Import errors**: Check virtual environment activation
4. **Static files not loading**: Run `python manage.py collectstatic`

### Debug Mode
Enable debug mode in `settings.py` for development:
```python
DEBUG = True
```

## 🔮 Future Enhancements

### Planned Features
- Real-time data sync with wearable devices
- Advanced machine learning models
- Social features and peer comparisons
- Healthcare provider integration
- Mobile app API endpoints

### Technical Improvements
- GraphQL API implementation
- Microservices architecture
- Real-time notifications
- Advanced caching strategies
- Performance optimization

## 📄 License

This project is developed for educational purposes and demonstrates modern web development practices in healthcare technology applications.

## 🙏 Acknowledgments

- **Django**: High-level Python web framework
- **Scikit-learn**: Machine learning library
- **Bootstrap**: Frontend framework
- **Chart.js**: Data visualization library

---

**Digital Twin of the Human Body — Student Edition Framework**  
*Empowering students with intelligent health monitoring and predictive analytics*

For questions, issues, or contributions, please refer to the project documentation or create an issue in the repository.

**Happy health tracking!** 🌟
