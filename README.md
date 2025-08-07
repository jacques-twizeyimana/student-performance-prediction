# Student Performance Prediction System

## Mission Statement

**Improve access to quality education for low-income families and rural households** by identifying key factors that influence student success and providing actionable insights for educational interventions.

## Problem

Educational inequality affects students from low-income and rural backgrounds. This ML system predicts student performance and identifies equity gaps to support evidence-based interventions.

## Dataset

**Source**: [Student Performance Factors Dataset (Kaggle)](https://www.kaggle.com/datasets/lainguyn123/student-performance-factors)

- **Size**: 1,000+ student records
- **Target**: Exam scores (0-100)
- **Features**: Study hours, attendance, family income, parental education, resource access, internet availability, sleep patterns, tutoring sessions, physical activity

## System Components

### 1. **Machine Learning Model** (`/summative/linear_regression/`)

- Trained Linear Regression, Decision Tree, and Random Forest models
- Best model: **R² = 0.87** (explains 87% of performance variance)
- Identifies socioeconomic factors affecting student success

### 2. **REST API** (`/summative/API/`)

- FastAPI backend with input validation and CORS support
- Predicts student scores and provides equity risk analysis
- **Live API**: [https://student-performance-m6la.onrender.com/docs](https://student-performance-m6la.onrender.com)

### 3. **Mobile App** (`/summative/flutterapp/`)

- Flutter app for educators and policymakers
- Input student data and receive predictions with recommendations

## Key Insights

- **Income Gap**: Low-income students score 8-12 points lower
- **Digital Divide**: No internet access reduces scores by 3-5 points
- **Resource Impact**: Limited educational resources reduce scores by 5-8 points
- **Parental Education**: College-educated parents correlate with 4-6 point improvement

## Live Demo

**[Video Demo](https://www.bugufi.link/IPaW3_)**

🌐 **API Endpoint**: `https://student-performance-m6la.onrender.com/predict`

## Quick Start

```bash
# 1. Train Model
cd summative/linear_regression/
jupyter notebook multivariate.ipynb

# 2. Start API
cd summative/API/
pip install -r requirements.txt
uvicorn prediction:app --reload

# 3. Run Mobile App
cd summative/FlutterApp/
flutter pub get && flutter run
```

## Impact

This system helps identify at-risk students and provides actionable recommendations to close the education gap for disadvantaged communities, supporting our mission of educational equity.

---

_🎯 Data-driven insights for educational equity and student success_
