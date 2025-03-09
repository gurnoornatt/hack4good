"""
Data routes for the BurnAI API.
These routes handle requests for raw and processed data.
"""
import os
import json
import logging
from typing import List, Dict, Any
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, Path, BackgroundTasks
import pandas as pd
import subprocess

# Create router
router = APIRouter(
    prefix="/data",
    tags=["data"],
    responses={404: {"description": "Not found"}},
)

# Setup logging
logger = logging.getLogger(__name__)


@router.get("/fire-points/{county_id}")
async def get_fire_points(county_id: str = Path(..., description="County identifier")):
    """
    Get recent fire points for a specific county.
    """
    try:
        # Path to NASA FIRMS data directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                               "data", "raw", "nasa")
        
        # Find the latest fire data file
        fire_file = None
        for file in os.listdir(data_dir):
            if file.endswith(".csv"):
                if fire_file is None or file > fire_file:
                    fire_file = file
        
        if fire_file is None:
            logger.warning(f"No fire data file found for county {county_id}")
            return {"message": "No fire data available", "points": []}
        
        # Load the data
        df = pd.read_csv(os.path.join(data_dir, fire_file))
        
        # Filter by county if county information is available in the data
        # This is a simplified example - in a real app, you would use geospatial filtering
        if "county_id" in df.columns:
            df = df[df["county_id"] == county_id]
        
        # Convert to list of dictionaries
        points = df.to_dict(orient="records")
        
        return {
            "county_id": county_id,
            "timestamp": datetime.now().isoformat(),
            "count": len(points),
            "points": points
        }
    
    except Exception as e:
        logger.error(f"Error getting fire points for county {county_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/weather/{county_id}")
async def get_weather(county_id: str = Path(..., description="County identifier")):
    """
    Get current weather conditions for a specific county.
    """
    try:
        # Path to NOAA data directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                               "data", "raw", "noaa")
        
        # Find the latest weather data file
        weather_file = None
        for file in os.listdir(data_dir):
            if file.endswith(".csv"):
                if weather_file is None or file > weather_file:
                    weather_file = file
        
        if weather_file is None:
            logger.warning(f"No weather data file found for county {county_id}")
            return {
                "county_id": county_id,
                "timestamp": datetime.now().isoformat(),
                "temperature": 22.0,
                "humidity": 60.0,
                "wind_speed": 10.0,
                "precipitation": 0.0
            }
        
        # Load the data
        df = pd.read_csv(os.path.join(data_dir, weather_file))
        
        # Filter by county if county information is available in the data
        if "county_id" in df.columns:
            county_data = df[df["county_id"] == county_id]
            if len(county_data) == 0:
                logger.warning(f"No weather data found for county {county_id}")
                return {
                    "county_id": county_id,
                    "timestamp": datetime.now().isoformat(),
                    "temperature": 22.0,
                    "humidity": 60.0,
                    "wind_speed": 10.0,
                    "precipitation": 0.0
                }
            
            # Get the latest record
            latest = county_data.iloc[-1]
            
            return {
                "county_id": county_id,
                "timestamp": datetime.now().isoformat(),
                "temperature": float(latest.get("temperature", 22.0)),
                "humidity": float(latest.get("humidity", 60.0)),
                "wind_speed": float(latest.get("wind_speed", 10.0)),
                "precipitation": float(latest.get("precipitation", 0.0))
            }
        
        # If county filtering is not possible, return default data
        return {
            "county_id": county_id,
            "timestamp": datetime.now().isoformat(),
            "temperature": 22.0,
            "humidity": 60.0,
            "wind_speed": 10.0,
            "precipitation": 0.0
        }
    
    except Exception as e:
        logger.error(f"Error getting weather for county {county_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/vegetation/{county_id}")
async def get_vegetation(county_id: str = Path(..., description="County identifier")):
    """
    Get vegetation data for a specific county.
    """
    try:
        # Path to vegetation data directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                               "data", "raw", "vegetation")
        
        # Find the latest vegetation data file
        veg_file = None
        for file in os.listdir(data_dir):
            if file.endswith(".csv"):
                if veg_file is None or file > veg_file:
                    veg_file = file
        
        if veg_file is None:
            logger.warning(f"No vegetation data file found for county {county_id}")
            return {
                "county_id": county_id,
                "timestamp": datetime.now().isoformat(),
                "vegetation_density": 0.5,
                "vegetation_type": "mixed",
                "ndvi_value": 0.4
            }
        
        # Load the data
        df = pd.read_csv(os.path.join(data_dir, veg_file))
        
        # Filter by county if county information is available in the data
        if "county_id" in df.columns:
            county_data = df[df["county_id"] == county_id]
            if len(county_data) == 0:
                logger.warning(f"No vegetation data found for county {county_id}")
                return {
                    "county_id": county_id,
                    "timestamp": datetime.now().isoformat(),
                    "vegetation_density": 0.5,
                    "vegetation_type": "mixed",
                    "ndvi_value": 0.4
                }
            
            # Get the latest record
            latest = county_data.iloc[-1]
            
            return {
                "county_id": county_id,
                "timestamp": datetime.now().isoformat(),
                "vegetation_density": float(latest.get("vegetation_density", 0.5)),
                "vegetation_type": latest.get("vegetation_type", "mixed"),
                "ndvi_value": float(latest.get("ndvi_value", 0.4))
            }
        
        # If county filtering is not possible, return default data
        return {
            "county_id": county_id,
            "timestamp": datetime.now().isoformat(),
            "vegetation_density": 0.5,
            "vegetation_type": "mixed",
            "ndvi_value": 0.4
        }
    
    except Exception as e:
        logger.error(f"Error getting vegetation data for county {county_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def run_data_collection():
    """
    Run the data collection script as a background task.
    """
    try:
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                  "collect_data.py")
        
        # Run the script
        result = subprocess.run(["python", script_path], 
                               capture_output=True, 
                               text=True)
        
        if result.returncode != 0:
            logger.error(f"Data collection failed: {result.stderr}")
            return False
        
        logger.info("Data collection completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error running data collection: {str(e)}")
        return False


def run_data_processing():
    """
    Run the data processing script as a background task.
    """
    try:
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                  "process_data.py")
        
        # Run the script
        result = subprocess.run(["python", script_path], 
                               capture_output=True, 
                               text=True)
        
        if result.returncode != 0:
            logger.error(f"Data processing failed: {result.stderr}")
            return False
        
        logger.info("Data processing completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error running data processing: {str(e)}")
        return False


def run_ai_analysis():
    """
    Run the AI analysis script as a background task.
    """
    try:
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                  "ai_analysis.py")
        
        # Run the script
        result = subprocess.run(["python", script_path], 
                               capture_output=True, 
                               text=True)
        
        if result.returncode != 0:
            logger.error(f"AI analysis failed: {result.stderr}")
            return False
        
        logger.info("AI analysis completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error running AI analysis: {str(e)}")
        return False


@router.post("/refresh")
async def refresh_data(background_tasks: BackgroundTasks):
    """
    Refresh all data by running collection, processing, and AI analysis.
    """
    try:
        # Add tasks to background queue
        background_tasks.add_task(run_data_collection)
        background_tasks.add_task(run_data_processing)
        background_tasks.add_task(run_ai_analysis)
        
        return {
            "message": "Data refresh started in the background",
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error starting data refresh: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") 