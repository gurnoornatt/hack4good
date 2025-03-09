"""
County routes for the BurnAI API.
These routes handle requests for county data, including burn assessments.
"""
import os
import json
import logging
from typing import List, Dict, Any
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, Path
import pandas as pd

from api.models.schemas import CountyBasic, CountyDetail, BurnAssessment, WeatherConditions, Limitation

# Create router
router = APIRouter(
    prefix="/counties",
    tags=["counties"],
    responses={404: {"description": "Not found"}},
)

# Setup logging
logger = logging.getLogger(__name__)

# Define county data (in a real app, this would come from a database)
COUNTIES = {
    "sf": {
        "id": "sf",
        "name": "San Francisco",
        "state": "California",
        "coordinates": {"lat": 37.7749, "lon": -122.4194}
    },
    "la": {
        "id": "la",
        "name": "Los Angeles",
        "state": "California",
        "coordinates": {"lat": 34.0522, "lon": -118.2437}
    }
}


def load_county_data() -> List[Dict[str, Any]]:
    """
    Load processed county data from CSV files.
    
    Returns:
        List of county data dictionaries
    """
    try:
        # Path to processed data directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                               "data", "processed")
        
        # Find the latest combined data file
        combined_file = None
        for file in os.listdir(data_dir):
            if file.startswith("combined_") and file.endswith(".csv"):
                if combined_file is None or file > combined_file:
                    combined_file = file
        
        if combined_file is None:
            logger.warning("No combined data file found")
            return []
        
        # Load the data
        df = pd.read_csv(os.path.join(data_dir, combined_file))
        
        # Convert to list of dictionaries
        counties = []
        for county_id in df["county_id"].unique():
            county_df = df[df["county_id"] == county_id].iloc[0]
            county_data = {
                "id": county_id,
                "name": COUNTIES.get(county_id, {}).get("name", "Unknown"),
                "state": COUNTIES.get(county_id, {}).get("state", "Unknown"),
                "suitability_score": float(county_df["suitability_score"]),
                "last_updated": datetime.now(),
                "fire_risk": float(county_df["fire_risk"]),
                "vegetation_density": float(county_df["vegetation_density"]),
                "historical_fires": int(county_df["historical_fires"]),
                "coordinates": COUNTIES.get(county_id, {}).get("coordinates", {"lat": 0, "lon": 0}),
                "weather": {
                    "temperature": float(county_df["temperature"]),
                    "humidity": float(county_df["humidity"]),
                    "wind_speed": float(county_df["wind_speed"]),
                    "precipitation": float(county_df["precipitation"]),
                    "date": datetime.now()
                },
                "limitations": [
                    {
                        "factor": "Weather",
                        "description": "Current weather conditions may affect burn operations",
                        "severity": "medium" if county_df["suitability_score"] < 70 else "low"
                    },
                    {
                        "factor": "Vegetation",
                        "description": "Vegetation density and type considerations",
                        "severity": "high" if county_df["vegetation_density"] > 0.7 else "medium"
                    }
                ]
            }
            counties.append(county_data)
        
        return counties
    
    except Exception as e:
        logger.error(f"Error loading county data: {str(e)}")
        return []


def load_assessment(county_id: str) -> Dict[str, Any]:
    """
    Load AI assessment for a specific county.
    
    Args:
        county_id: County identifier
        
    Returns:
        Assessment data dictionary
    """
    try:
        # Path to assessments directory
        assessments_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                      "data", "assessments")
        
        # Find the latest assessment file for this county
        assessment_file = None
        for file in os.listdir(assessments_dir):
            if file.startswith(f"{county_id}_") and file.endswith(".json"):
                if assessment_file is None or file > assessment_file:
                    assessment_file = file
        
        if assessment_file is None:
            logger.warning(f"No assessment file found for county {county_id}")
            return {}
        
        # Load the assessment
        with open(os.path.join(assessments_dir, assessment_file), "r") as f:
            assessment = json.load(f)
        
        return assessment
    
    except Exception as e:
        logger.error(f"Error loading assessment for county {county_id}: {str(e)}")
        return {}


@router.get("/", response_model=List[CountyBasic])
async def get_counties():
    """
    Get a list of all counties with basic information.
    """
    try:
        counties = load_county_data()
        if not counties:
            # Return default data if no processed data is available
            return [
                CountyBasic(
                    id=county_id,
                    name=data["name"],
                    state=data["state"],
                    suitability_score=75.0,  # Default score
                    last_updated=datetime.now()
                )
                for county_id, data in COUNTIES.items()
            ]
        
        return [
            CountyBasic(
                id=county["id"],
                name=county["name"],
                state=county["state"],
                suitability_score=county["suitability_score"],
                last_updated=county["last_updated"]
            )
            for county in counties
        ]
    
    except Exception as e:
        logger.error(f"Error in get_counties: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{county_id}", response_model=CountyDetail)
async def get_county(county_id: str = Path(..., description="County identifier")):
    """
    Get detailed information about a specific county.
    """
    try:
        if county_id not in COUNTIES:
            raise HTTPException(status_code=404, detail=f"County {county_id} not found")
        
        counties = load_county_data()
        county_data = next((c for c in counties if c["id"] == county_id), None)
        
        if not county_data:
            # Return default data if no processed data is available
            return CountyDetail(
                id=county_id,
                name=COUNTIES[county_id]["name"],
                state=COUNTIES[county_id]["state"],
                suitability_score=75.0,  # Default score
                last_updated=datetime.now(),
                weather=WeatherConditions(
                    temperature=22.0,
                    humidity=60.0,
                    wind_speed=10.0,
                    precipitation=0.0,
                    date=datetime.now()
                ),
                fire_risk=0.3,
                vegetation_density=0.5,
                historical_fires=5,
                limitations=[
                    Limitation(
                        factor="Weather",
                        description="Default weather limitations",
                        severity="medium"
                    )
                ],
                coordinates=COUNTIES[county_id]["coordinates"]
            )
        
        return CountyDetail(
            id=county_data["id"],
            name=county_data["name"],
            state=county_data["state"],
            suitability_score=county_data["suitability_score"],
            last_updated=county_data["last_updated"],
            weather=WeatherConditions(**county_data["weather"]),
            fire_risk=county_data["fire_risk"],
            vegetation_density=county_data["vegetation_density"],
            historical_fires=county_data["historical_fires"],
            limitations=[Limitation(**l) for l in county_data["limitations"]],
            coordinates=county_data["coordinates"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_county: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{county_id}/assessment", response_model=BurnAssessment)
async def get_assessment(county_id: str = Path(..., description="County identifier")):
    """
    Get AI-generated burn assessment for a specific county.
    """
    try:
        if county_id not in COUNTIES:
            raise HTTPException(status_code=404, detail=f"County {county_id} not found")
        
        assessment = load_assessment(county_id)
        
        if not assessment:
            # Return default assessment if no AI assessment is available
            return BurnAssessment(
                county_id=county_id,
                county_name=COUNTIES[county_id]["name"],
                timestamp=datetime.now(),
                overall_recommendation="No assessment available. Please run the AI analysis.",
                suitability_score=50.0,
                key_factors=[
                    {"name": "Default Factor", "value": 0.5, "weight": 1.0}
                ],
                limitations=[
                    Limitation(
                        factor="Data",
                        description="No assessment data available",
                        severity="high"
                    )
                ],
                recommendations=["Run the AI analysis to get recommendations"],
                weather_impact="Unknown without assessment",
                vegetation_analysis="Unknown without assessment",
                historical_context="Unknown without assessment"
            )
        
        # Convert timestamp string to datetime if needed
        if isinstance(assessment.get("timestamp"), str):
            assessment["timestamp"] = datetime.fromisoformat(assessment["timestamp"].replace("Z", "+00:00"))
        
        return BurnAssessment(**assessment)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_assessment: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") 