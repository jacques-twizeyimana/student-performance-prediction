# 🚀 Student Performance Prediction

## 📋 Overview

This FastAPI application predicts student exam performance based on socioeconomic and educational factors, supporting our mission to improve access to quality education for low-income families and rural households.

## 🎯 Mission Statement

**"Improve access to quality education for low-income families and rural households by identifying key factors that influence student success and providing actionable insights for educational interventions."**

## 📁 Project Structure

```
summative/
├── linear_regression/
│   └── multivariate.ipynb          # Your completed linear regression notebook
├── API/
│   ├── prediction.py               # Main FastAPI application
│   ├── requirements.txt            # Python dependencies
│   ├── test_api.py                 # API testing script
│   └── render.yaml                 # Render deployment config
└── model_files/                    # Generated from notebook
    ├── best_student_performance_model.pkl
    ├── feature_scaler.pkl
    ├── label_encoders.pkl
    └── feature_names.pkl
```

## 🔧 Local Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Completed linear regression notebook (Task 1)

### Step 1: Install Dependencies

```bash
cd API/
pip install -r requirements.txt
```

### Step 2: Ensure Model Files Exist

Make sure you've run your linear regression notebook and generated these files:

- `best_student_performance_model.pkl`
- `feature_scaler.pkl`
- `label_encoders.pkl`
- `feature_names.pkl`

Copy these files to your API directory or update the file paths in `prediction.py`.

### Step 3: Run the API Locally

```bash
uvicorn prediction:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Test the API

```bash
# In a new terminal
python test_api.py
```

### Step 5: Access Swagger UI

Open your browser and navigate to:

- **Local Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Health**: http://localhost:8000/health

## 🌐 Deployment on Render

### Step 1: Prepare Repository

1. Create a GitHub repository
2. Upload your code with this structure:

```
repository/
├── summative/
│   ├── linear_regression/
│   │   └── multivariate.ipynb
│   ├── API/
│   │   ├── prediction.py
│   │   ├── requirements.txt
│   │   └── render.yaml
│   └── FlutterApp/
├── best_student_performance_model.pkl
├── feature_scaler.pkl
├── label_encoders.pkl
├── feature_names.pkl
└── README.md
```

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com)
2. Sign up/Login with your GitHub account
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure deployment:
   - **Name**: `student-performance-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r summative/API/requirements.txt`
   - **Start Command**: `uvicorn summative.API.prediction:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free tier is sufficient

### Step 3: Environment Variables (if needed)

Add these in Render dashboard:

- `PYTHON_VERSION`: `3.9.18`
- Any other custom environment variables

### Step 4: Deploy

- Click "Create Web Service"
- Wait for deployment (5-10 minutes)
- Your API will be available at: `https://your-service-name.onrender.com`

## 🧪 API Testing

### Endpoints Overview

- `GET /` - API information
- `GET /health` - Health check
- `GET /model-info` - Model details
- `POST /predict` - Main prediction endpoint

### Example API Calls

#### Health Check

```bash
curl https://your-api-url.onrender.com/health
```

#### Prediction for Low-Income Student

```bash
curl -X POST "https://your-api-url.onrender.com/predict" \
-H "Content-Type: application/json" \
-d '{
  "hours_studied": 4.0,
  "attendance": 75.0,
  "parental_involvement": "Low",
  "access_to_resources": "Low",
  "sleep_hours": 6.5,
  "previous_scores": 65.0,
  "tutoring_sessions": 0.5,
  "family_income": "Low",
  "parental_education_level": "High School",
  "internet_access": "No",
  "physical_activity": 1.5
}'
```

#### Prediction for Privileged Student

```bash
curl -X POST "https://your-api-url.onrender.com/predict" \
-H "Content-Type: application/json" \
-d '{
  "hours_studied": 8.0,
  "attendance": 95.0,
  "parental_involvement": "High",
  "access_to_resources": "High",
  "sleep_hours": 8.0,
  "previous_scores": 85.0,
  "tutoring_sessions": 3.0,
  "family_income": "High",
  "parental_education_level": "Postgraduate",
  "internet_access": "Yes",
  "physical_activity": 4.0
}'
```

## 📊 Input Validation & Constraints

### Numerical Fields

| Field             | Type  | Range       | Description              |
| ----------------- | ----- | ----------- | ------------------------ |
| hours_studied     | float | 0.0 - 20.0  | Weekly study hours       |
| attendance        | float | 0.0 - 100.0 | Attendance percentage    |
| sleep_hours       | float | 3.0 - 12.0  | Nightly sleep hours      |
| previous_scores   | float | 0.0 - 100.0 | Previous academic scores |
| tutoring_sessions | float | 0.0 - 10.0  | Weekly tutoring sessions |
| physical_activity | float | 0.0 - 15.0  | Weekly activity hours    |

### Categorical Fields

| Field                    | Valid Values                             |
| ------------------------ | ---------------------------------------- |
| parental_involvement     | "Low", "Medium", "High"                  |
| access_to_resources      | "Low", "Medium", "High"                  |
| family_income            | "Low", "Medium", "High"                  |
| parental_education_level | "High School", "College", "Postgraduate" |
| internet_access          | "Yes", "No"                              |

## 🔍 Testing Data Types and Ranges

### Valid Test Cases

```json
{
  "hours_studied": 6.0,
  "attendance": 85.0,
  "parental_involvement": "Medium",
  "access_to_resources": "Medium",
  "sleep_hours": 7.0,
  "previous_scores": 75.0,
  "tutoring_sessions": 2.0,
  "family_income": "Medium",
  "parental_education_level": "College",
  "internet_access": "Yes",
  "physical_activity": 3.0
}
```

### Invalid Test Cases (Should Return 422)

```json
{
  "hours_studied": -5.0, // Negative value
  "attendance": 150.0, // Above 100
  "parental_involvement": "Very High", // Invalid category
  "sleep_hours": 1.0, // Below minimum
  "tutoring_sessions": 15.0 // Above maximum
}
```

## 🎯 Mission-Aligned Features

### Equity Risk Factor Detection

The API automatically identifies students at risk due to:

- Low family income
- Limited access to resources
- No internet access
- Low parental education
- Minimal parental involvement

### Personalized Recommendations

Provides actionable suggestions for:

- Study time optimization
- Attendance improvement
- Sleep and wellness
- Academic support needs
- Resource access solutions

### Policy Insights

Generates insights for:

- Intervention priority levels
- Support system assessment
- Economic impact analysis
- Resource allocation needs

## 🐛 Troubleshooting

### Common Issues

#### 1. Model Files Not Found

```
Error: Model not loaded. Please ensure model files are available.
```

**Solution**: Ensure model files are in the correct directory and paths are updated in `prediction.py`.

#### 2. Import Errors

```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**: Install requirements: `pip install -r requirements.txt`

#### 3. Port Already in Use

```
Error: Port 8000 is already in use
```

**Solution**: Use different port: `uvicorn prediction:app --port 8001`

#### 4. CORS Issues

**Solution**: CORS is configured for all origins (`"*"`). For production, specify actual frontend URLs.

### Deployment Issues

#### 1. Build Fails on Render

- Check `requirements.txt` formatting
- Ensure Python version compatibility
- Verify file paths in start command

#### 2. Model Loading Fails

- Ensure model files are committed to repository
- Check file paths are relative to project root
- Verify files aren't ignored by `.gitignore`

## 📈 API Response Format

### Successful Prediction Response

```json
{
  "predicted_score": 78.45,
  "performance_level": "Good",
  "recommendations": [
    "Increase weekly study time to at least 5-6 hours for better performance",
    "Consider additional tutoring sessions for personalized academic support"
  ],
  "equity_risk_factors": [
    "Low family income may limit access to educational resources",
    "Limited access to educational resources requires community support"
  ],
  "mission_insights": {
    "income_impact": "Economic barriers may significantly impact educational outcomes",
    "resource_access": "Critical resource limitations requiring immediate intervention",
    "support_needed": true,
    "intervention_priority": "High"
  },
  "confidence_level": "High"
}
```

### Error Response

```json
{
  "detail": [
    {
      "loc": ["body", "hours_studied"],
      "msg": "ensure this value is greater than or equal to 0",
      "type": "value_error.number.not_ge",
      "ctx": { "limit_value": 0 }
    }
  ]
}
```

## 🔗 Next Steps

After successful API deployment:

1. ✅ Test all endpoints via Swagger UI
2. ✅ Verify data validation works correctly
3. ✅ Test with various student profiles
4. ✅ Note your public API URL for Flutter app (Task 3)
5. ✅ Prepare for video demonstration (Task 4)

## 📞 Support

For issues or questions:

- Check Swagger UI documentation: `/docs`
- Review API health: `/health`
- Test with provided examples
- Verify model files are properly loaded

---

**🎓 This API supports evidence-based educational interventions to close the achievement gap for disadvantaged students.**
