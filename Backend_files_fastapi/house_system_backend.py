# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
from typing import List, Dict

# Create APIRouter instance
router = APIRouter(
    prefix="/house",
    tags=["House Price Prediction"],
    responses={404: {"description": "Not found"}}
)

# Load artifacts
try:
    model = joblib.load('best_house_price_model.joblib')
    scaler = joblib.load('scaler.joblib')
    encoders = joblib.load('label_encoders.joblib')
except Exception as e:
    raise RuntimeError(f"Error loading artifacts: {e}")

# --- Define request schema with validation ---
class HouseFeatures(BaseModel):
    area: int = Field(..., gt=0, description="Area in square feet")
    bedrooms: int = Field(..., gt=0, description="Number of bedrooms")
    bathrooms: int = Field(..., gt=0, description="Number of bathrooms")
    stories: int = Field(..., gt=0, description="Number of stories")
    mainroad: str = Field(..., description="Main road access (yes/no)")
    guestroom: str = Field(..., description="Guest room available (yes/no)")
    basement: str = Field(..., description="Basement available (yes/no)")
    hotwaterheating: str = Field(..., description="Hot water heating (yes/no)")
    airconditioning: str = Field(..., description="Air conditioning (yes/no)")
    parking: int = Field(..., ge=0, description="Number of parking spots")
    furnishingstatus: str = Field(..., description="Furnishing status")
    city: str = Field(..., description="City name")
    year_built: int = Field(..., gt=1800, lt=2025, description="Year built")

    # Add example for Swagger
    class Config:
        schema_extra = {
            "example": {
                "area": 7420,
                "bedrooms": 4,
                "bathrooms": 2,
                "stories": 3,
                "mainroad": "yes",
                "guestroom": "no",
                "basement": "no",
                "hotwaterheating": "no",
                "airconditioning": "yes",
                "parking": 2,
                "furnishingstatus": "furnished",
                "city": "Seattle",
                "year_built": 2014
            }
        }

# --- Response schema ---
class HousePriceResponse(BaseModel):
    predicted_price: float = Field(..., description="Predicted house price")
    features_used: dict = Field(..., description="Features used for prediction")

# --- Endpoint logic ---
@router.post(
    "/predict",
    response_model=HousePriceResponse,
    summary="Predict house price",
    description="Predict house price based on property features",
    response_description="Prediction result with price"
)
def predict_house_price(features: HouseFeatures):
    """
    Predict the price of a house based on its features:

    - **area**: Property area in square feet
    - **bedrooms**: Number of bedrooms
    - **bathrooms**: Number of bathrooms
    - **stories**: Number of stories
    - **mainroad**: Access to main road (yes/no)
    - **guestroom**: Guest room available (yes/no)
    - **basement**: Basement available (yes/no)
    - **hotwaterheating**: Hot water heating available (yes/no)
    - **airconditioning**: Air conditioning available (yes/no)
    - **parking**: Number of parking spots
    - **furnishingstatus**: Furnishing status (furnished, semi-furnished, unfurnished)
    - **city**: City name
    - **year_built**: Year the property was built
    """
    try:
        # Convert to DataFrame
        input_data = pd.DataFrame([features.dict()])

        # Feature engineering
        input_data['age'] = 2025 - input_data['year_built']
        input_data['renovated'] = 0

        # Encode categorical features
        cat_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating',
                    'airconditioning', 'furnishingstatus', 'city']

        for col in cat_cols:
            # Handle unseen categories
            if input_data[col].iloc[0] not in encoders[col].classes_:
                default_value = encoders[col].classes_[0]
                input_data[col] = default_value
            input_data[col] = encoders[col].transform(input_data[col])

        input_data.drop('year_built', axis=1, inplace=True)

        # Scale features
        scaled_data = scaler.transform(input_data)

        # Predict
        prediction = model.predict(scaled_data)[0]

        return HousePriceResponse(
            predicted_price=float(prediction),
            features_used=features.dict()
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@router.get(
    "/cities",
    response_model=List[str],
    summary="Get supported cities",
    description="Retrieve list of supported cities for prediction"
)
def get_supported_cities():
    """Return list of supported cities"""
    try:
        return sorted(encoders['city'].classes_.tolist())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving cities: {str(e)}")

@router.get(
    "/furnishing-options",
    response_model=List[str],
    summary="Get furnishing options",
    description="Retrieve available furnishing status options"
)
def get_furnishing_options():
    """Return furnishing status options"""
    try:
        return sorted(encoders['furnishingstatus'].classes_.tolist())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving options: {str(e)}")
