# Student Performance Prediction API
# Mission: Improve access to quality education for low-income families and rural households

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import joblib
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import os

# Initialize FastAPI app
app = FastAPI(
    title="Student Performance Prediction API",
    description="""
    This API predicts student exam performance based on various socioeconomic and educational factors.
    
    **Mission**: Improve access to quality education for low-income families and rural households
    by identifying key factors that influence student success and providing actionable insights
    for educational interventions.
    
    **Features**:
    - Predicts student exam scores (0-100)
    - Identifies equity risk factors for disadvantaged students
    - Provides personalized recommendations for improvement
    - Supports evidence-based educational policy decisions
    """,
    version="1.0.0",
    contact={
        "name": "Educational Equity Research Team",
        "email": "contact@education-equity.org"
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model components
model = None
scaler = None
label_encoders = None
feature_names = None

# Load model components on startup
@app.on_event("startup")
async def load_model():
    """Load the trained model and preprocessing components on app startup."""
    global model, scaler, label_encoders, feature_names
    
    try:
        # Load model components (adjust paths as needed)
        model = joblib.load('best_student_performance_model.pkl')
        scaler = joblib.load('feature_scaler.pkl')
        label_encoders = joblib.load('label_encoders.pkl')
        feature_names = joblib.load('feature_names.pkl')
        print("✅ Model components loaded successfully")
    except FileNotFoundError as e:
        print(f"❌ Error loading model components: {e}")
        print("🔧 Make sure to run the linear regression notebook first to generate model files")

# Pydantic models for request/response validation
class StudentInput(BaseModel):
    """
    Input model for student performance prediction with data validation and constraints.
    """
    hours_studied: float = Field(
        ..., 
        ge=0.0, 
        le=20.0, 
        description="Number of hours studied per week (0-20 hours)"
    )
    attendance: float = Field(
        ..., 
        ge=0.0, 
        le=100.0, 
        description="Attendance percentage (0-100%)"
    )
    parental_involvement: str = Field(
        ..., 
        description="Level of parental involvement in education"
    )
    access_to_resources: str = Field(
        ..., 
        description="Student's access to educational resources"
    )
    sleep_hours: float = Field(
        ..., 
        ge=3.0, 
        le=12.0, 
        description="Average sleep hours per night (3-12 hours)"
    )
    previous_scores: float = Field(
        ..., 
        ge=0.0, 
        le=100.0, 
        description="Previous academic scores (0-100)"
    )
    tutoring_sessions: float = Field(
        ..., 
        ge=0.0, 
        le=10.0, 
        description="Number of tutoring sessions per week (0-10)"
    )
    family_income: str = Field(
        ..., 
        description="Family income level"
    )
    parental_education_level: str = Field(
        ..., 
        description="Highest education level of parents"
    )
    internet_access: str = Field(
        ..., 
        description="Whether student has internet access"
    )
    physical_activity: float = Field(
        ..., 
        ge=0.0, 
        le=15.0, 
        description="Hours of physical activity per week (0-15 hours)"
    )
    
    @field_validator('parental_involvement')
    @classmethod
    def validate_parental_involvement(cls, v):
        allowed_values = ['Low', 'Medium', 'High']
        if v not in allowed_values:
            raise ValueError(f'parental_involvement must be one of {allowed_values}')
        return v
    
    @field_validator('access_to_resources')
    @classmethod
    def validate_access_to_resources(cls, v):
        allowed_values = ['Low', 'Medium', 'High']
        if v not in allowed_values:
            raise ValueError(f'access_to_resources must be one of {allowed_values}')
        return v
    
    @field_validator('family_income')
    @classmethod
    def validate_family_income(cls, v):
        allowed_values = ['Low', 'Medium', 'High']
        if v not in allowed_values:
            raise ValueError(f'family_income must be one of {allowed_values}')
        return v
    
    @field_validator('parental_education_level')
    @classmethod
    def validate_parental_education_level(cls, v):
        allowed_values = ['High School', 'College', 'Postgraduate']
        if v not in allowed_values:
            raise ValueError(f'parental_education_level must be one of {allowed_values}')
        return v
    
    @field_validator('internet_access')
    @classmethod
    def validate_internet_access(cls, v):
        allowed_values = ['Yes', 'No']
        if v not in allowed_values:
            raise ValueError(f'internet_access must be one of {allowed_values}')
        return v

class MissionInsights(BaseModel):
    """Mission-specific insights for educational equity."""
    income_impact: str
    resource_access: str
    support_needed: bool
    intervention_priority: str

class PredictionResponse(BaseModel):
    """Response model for prediction results."""
    predicted_score: float = Field(..., description="Predicted exam score (0-100)")
    performance_level: str = Field(..., description="Performance category")
    recommendations: List[str] = Field(..., description="Actionable recommendations for improvement")
    equity_risk_factors: List[str] = Field(..., description="Risk factors affecting educational equity")
    mission_insights: MissionInsights = Field(..., description="Insights aligned with educational equity mission")
    confidence_level: str = Field(..., description="Model confidence in prediction")

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    message: str
    is_model_loaded: bool

# API Routes

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Student Performance Prediction API",
        "mission": "Improve access to quality education for low-income families and rural households",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify API and model status."""
    model_loaded = all([model is not None, scaler is not None, 
                       label_encoders is not None, feature_names is not None])
    
    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        message="API is running and model is loaded" if model_loaded else "API is running but model not loaded",
        is_model_loaded=model_loaded
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_student_performance(student_data: StudentInput):
    """
    Predict student exam performance based on various factors.
    
    This endpoint supports our mission to improve access to quality education
    for low-income families and rural households by identifying key factors
    that influence student success and providing actionable recommendations.
    
    **Input Parameters:**
    - **hours_studied**: Weekly study hours (0-20)
    - **attendance**: Attendance percentage (0-100)
    - **parental_involvement**: Level of parental involvement (Low/Medium/High)
    - **access_to_resources**: Access to educational resources (Low/Medium/High)
    - **sleep_hours**: Average sleep hours per night (3-12)
    - **previous_scores**: Previous academic scores (0-100)
    - **tutoring_sessions**: Weekly tutoring sessions (0-10)
    - **family_income**: Family income level (Low/Medium/High)
    - **parental_education_level**: Parents' education (High School/College/Postgraduate)
    - **internet_access**: Internet access (Yes/No)
    - **physical_activity**: Weekly physical activity hours (0-15)
    
    **Returns:**
    - Predicted exam score and performance level
    - Personalized recommendations for improvement
    - Equity risk factors identification
    - Mission-aligned insights for intervention planning
    """
    
    # Check if model is loaded
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded. Please ensure model files are available."
        )
    
    try:
        # Convert input to DataFrame with exact column names from training
        input_data = pd.DataFrame({
            'Hours_Studied': [student_data.hours_studied],
            'Attendance': [student_data.attendance],
            'Parental_Involvement': [student_data.parental_involvement],
            'Access_to_Resources': [student_data.access_to_resources],
            'Sleep_Hours': [student_data.sleep_hours],
            'Previous_Scores': [student_data.previous_scores],
            'Tutoring_Sessions': [student_data.tutoring_sessions],
            'Family_Income': [student_data.family_income],
            'Parental_Education_Level': [student_data.parental_education_level],
            'Internet_Access': [student_data.internet_access],
            'Physical_Activity': [student_data.physical_activity]
        })
        
        print(f"Debug - Input data before encoding: {input_data.to_dict()}")
        
        # Encode categorical variables using the SAME encoders from training
        categorical_columns = ['Parental_Involvement', 'Access_to_Resources', 'Family_Income', 
                             'Parental_Education_Level', 'Internet_Access']
        
        for col in categorical_columns:
            if col in label_encoders and col in input_data.columns:
                try:
                    # Get the original value for debugging
                    original_value = input_data[col].iloc[0]
                    # Transform using the saved encoder
                    encoded_value = label_encoders[col].transform(input_data[col])[0]
                    input_data[col] = encoded_value
                    print(f"Debug - Encoded {col}: '{original_value}' -> {encoded_value}")
                except ValueError as e:
                    # Handle unseen categories - use the most common class (usually 0)
                    print(f"Warning - Unseen category in {col}: {input_data[col].iloc[0]}")
                    input_data[col] = 0
        
        print(f"Debug - Input data after encoding: {input_data.to_dict()}")
        
        # Create engineered features EXACTLY as in training
        # Only create features that exist in feature_names
        if 'Study_Efficiency' in feature_names:
            efficiency = input_data['Hours_Studied'].iloc[0] / (input_data['Attendance'].iloc[0] + 1)
            input_data['Study_Efficiency'] = efficiency
            print(f"Debug - Study_Efficiency: {efficiency}")
        
        if 'Support_System_Score' in feature_names:
            support_score = 0
            if 'Parental_Involvement' in input_data.columns:
                support_score += input_data['Parental_Involvement'].iloc[0]
            if 'Tutoring_Sessions' in input_data.columns:
                support_score += input_data['Tutoring_Sessions'].iloc[0]
            if 'Access_to_Resources' in input_data.columns:
                support_score += input_data['Access_to_Resources'].iloc[0]
            input_data['Support_System_Score'] = support_score
            print(f"Debug - Support_System_Score: {support_score}")
        
        if 'Wellbeing_Score' in feature_names:
            wellbeing = input_data['Sleep_Hours'].iloc[0] + input_data['Physical_Activity'].iloc[0]
            input_data['Wellbeing_Score'] = wellbeing
            print(f"Debug - Wellbeing_Score: {wellbeing}")
        
        print(f"Debug - Feature names from training: {feature_names}")
        print(f"Debug - Available columns: {list(input_data.columns)}")
        
        # Select and order features to EXACTLY match training
        # This is critical - must be in same order and same features
        final_features = []
        for feature in feature_names:
            if feature in input_data.columns:
                final_features.append(input_data[feature].iloc[0])
            else:
                print(f"Warning - Missing feature: {feature}, using 0")
                final_features.append(0.0)
        
        # Convert to numpy array with correct shape
        input_array = np.array(final_features).reshape(1, -1)
        print(f"Debug - Input array shape: {input_array.shape}")
        print(f"Debug - Input array values: {input_array}")
        
        # Scale features using the SAME scaler from training
        input_scaled = scaler.transform(input_array)
        print(f"Debug - Scaled input shape: {input_scaled.shape}")
        print(f"Debug - Scaled input values: {input_scaled}")
        
        # Make prediction
        raw_prediction = model.predict(input_scaled)[0]
        print(f"Debug - Raw prediction: {raw_prediction}")
        
        # Convert to float and ensure reasonable range
        prediction = float(raw_prediction)
        
        # Handle extreme predictions (likely due to data issues)
        if abs(prediction) > 1000:  # If prediction is unreasonably large
            print(f"Warning - Extreme prediction detected: {prediction}")
            # Use a fallback prediction based on input features
            fallback = (
                student_data.previous_scores * 0.4 +  # 40% weight on previous scores
                (student_data.hours_studied / 20 * 30) +  # 30% weight on study hours
                (student_data.attendance / 100 * 20) +  # 20% weight on attendance  
                (7 if student_data.family_income == 'High' else 3 if student_data.family_income == 'Medium' else -3) +  # Income impact
                (5 if student_data.access_to_resources == 'High' else 0 if student_data.access_to_resources == 'Medium' else -5)  # Resource impact
            )
            prediction = max(0, min(100, fallback))
            print(f"Using fallback prediction: {prediction}")
        else:
            # Normal case - just ensure it's in valid range
            prediction = max(0.0, min(100.0, prediction))
        
        print(f"Debug - Final prediction: {prediction}")
        
        # Generate performance level
        if prediction >= 85:
            performance_level = "Excellent"
            confidence = "High"
        elif prediction >= 75:
            performance_level = "Good"
            confidence = "High"
        elif prediction >= 65:
            performance_level = "Average"
            confidence = "Medium"
        elif prediction >= 50:
            performance_level = "Below Average"
            confidence = "Medium"
        else:
            performance_level = "Needs Significant Improvement"
            confidence = "Low"
        
        # Generate recommendations
        recommendations = []
        
        if student_data.hours_studied < 5:
            recommendations.append("Increase weekly study time to at least 5-6 hours for better performance")
        if student_data.attendance < 80:
            recommendations.append("Improve attendance rate - aim for at least 85% to maximize learning")
        if student_data.sleep_hours < 7:
            recommendations.append("Ensure adequate sleep (7-8 hours) for optimal cognitive performance")
        if student_data.tutoring_sessions < 1:
            recommendations.append("Consider additional tutoring sessions for personalized academic support")
        if student_data.physical_activity < 2:
            recommendations.append("Include regular physical activity (2-3 hours/week) to improve focus and health")
        if student_data.previous_scores < 70:
            recommendations.append("Focus on strengthening foundational knowledge in weak subject areas")
        
        if not recommendations:
            recommendations.append("Continue current study habits and maintain consistent performance")
        
        # Identify equity risk factors (mission-aligned)
        equity_risk_factors = []
        
        if student_data.family_income == 'Low':
            equity_risk_factors.append("Low family income may limit access to educational resources and opportunities")
        if student_data.access_to_resources == 'Low':
            equity_risk_factors.append("Limited access to educational resources requires community support programs")
        if student_data.internet_access == 'No':
            equity_risk_factors.append("Lack of internet access creates significant barriers in digital learning environment")
        if student_data.parental_education_level == 'High School':
            equity_risk_factors.append("Limited parental education may require additional family engagement programs")
        if student_data.parental_involvement == 'Low':
            equity_risk_factors.append("Low parental involvement indicates need for family engagement initiatives")
        
        if not equity_risk_factors:
            equity_risk_factors.append("No significant equity risk factors identified - student has good support systems")
        
        # Mission insights
        income_impact = "Economic barriers may significantly impact educational outcomes" if student_data.family_income == 'Low' else \
                       "Moderate economic impact on educational access" if student_data.family_income == 'Medium' else \
                       "Economic factors are supportive of educational success"
        
        resource_access = "Critical resource limitations requiring immediate intervention" if student_data.access_to_resources == 'Low' else \
                         "Moderate resource access with room for improvement" if student_data.access_to_resources == 'Medium' else \
                         "Good access to educational resources supporting success"
        
        support_needed = len(equity_risk_factors) > 2 and student_data.family_income == 'Low'
        
        intervention_priority = "High" if support_needed else \
                              "Medium" if len(equity_risk_factors) > 1 else "Low"
        
        mission_insights = MissionInsights(
            income_impact=income_impact,
            resource_access=resource_access,
            support_needed=support_needed,
            intervention_priority=intervention_priority
        )
        
        return PredictionResponse(
            predicted_score=round(prediction, 2),
            performance_level=performance_level,
            recommendations=recommendations,
            equity_risk_factors=equity_risk_factors,
            mission_insights=mission_insights,
            confidence_level=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

@app.get("/model-info", response_model=Dict[str, Any])
async def get_model_info():
    """Get information about the loaded model and its capabilities."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": type(model).__name__,
        "features_count": len(feature_names) if feature_names else 0,
        "feature_names": feature_names if feature_names else [],
        "categorical_features": list(label_encoders.keys()) if label_encoders else [],
        "scaling_method": "StandardScaler",
        "mission": "Improve access to quality education for low-income families and rural households",
        "prediction_range": "0-100 (exam scores)",
        "supported_inputs": {
            "hours_studied": "0-20 hours per week",
            "attendance": "0-100 percentage",
            "parental_involvement": ["Low", "Medium", "High"],
            "access_to_resources": ["Low", "Medium", "High"],
            "sleep_hours": "3-12 hours per night",
            "previous_scores": "0-100 points",
            "tutoring_sessions": "0-10 sessions per week",
            "family_income": ["Low", "Medium", "High"],
            "parental_education_level": ["High School", "College", "Postgraduate"],
            "internet_access": ["Yes", "No"],
            "physical_activity": "0-15 hours per week"
        }
    }

# Error handlers
@app.exception_handler(422)
async def validation_exception_handler(request, exc):
    """Custom handler for validation errors with helpful messages."""
    return {
        "error": "Validation Error",
        "message": "Please check your input values and ensure they meet the specified constraints",
        "details": exc.errors(),
        "help": "Visit /docs for detailed API documentation and valid input ranges"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)