"""
Pydantic models for the BurnAI API.
These models define the structure of request and response data.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class WeatherConditions(BaseModel):
    """Weather conditions for a specific location."""
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Relative humidity percentage")
    wind_speed: float = Field(..., description="Wind speed in km/h")
    precipitation: float = Field(..., description="Precipitation in mm")
    date: datetime = Field(..., description="Date of the weather data")


class Limitation(BaseModel):
    """Limitation for controlled burns."""
    factor: str = Field(..., description="Limiting factor")
    description: str = Field(..., description="Description of the limitation")
    severity: str = Field(..., description="Severity of the limitation (low, medium, high)")


class CountyBasic(BaseModel):
    """Basic information about a county."""
    id: str = Field(..., description="County identifier")
    name: str = Field(..., description="County name")
    state: str = Field(..., description="State name")
    suitability_score: float = Field(..., description="Overall suitability score for controlled burns")
    last_updated: datetime = Field(..., description="Last data update timestamp")


class CountyDetail(CountyBasic):
    """Detailed information about a county."""
    weather: WeatherConditions = Field(..., description="Current weather conditions")
    fire_risk: float = Field(..., description="Current fire risk score")
    vegetation_density: float = Field(..., description="Vegetation density score")
    historical_fires: int = Field(..., description="Number of historical fires in the past year")
    limitations: List[Limitation] = Field(..., description="Limitations for controlled burns")
    coordinates: Dict[str, float] = Field(..., description="Geographic coordinates (lat, lon)")


class BurnAssessment(BaseModel):
    """AI-generated assessment for controlled burns."""
    county_id: str = Field(..., description="County identifier")
    county_name: str = Field(..., description="County name")
    timestamp: datetime = Field(..., description="Assessment generation timestamp")
    overall_recommendation: str = Field(..., description="Overall recommendation")
    suitability_score: float = Field(..., description="Suitability score (0-100)")
    key_factors: List[Dict[str, Any]] = Field(..., description="Key factors influencing the assessment")
    limitations: List[Limitation] = Field(..., description="Limitations for controlled burns")
    recommendations: List[str] = Field(..., description="Specific recommendations")
    weather_impact: str = Field(..., description="Impact of current weather conditions")
    vegetation_analysis: str = Field(..., description="Analysis of vegetation conditions")
    historical_context: str = Field(..., description="Historical context of fires in the area")


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(..., description="Error detail message")
    status_code: int = Field(..., description="HTTP status code")
    path: Optional[str] = Field(None, description="Request path")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp") 