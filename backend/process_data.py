#!/usr/bin/env python3
"""
BurnAI Data Processing Script

This script processes the collected data from various sources,
merges them based on geographic coordinates, and prepares them for AI analysis.
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
from datetime import datetime
import glob
from dotenv import load_dotenv
from shapely.geometry import Point
import geopandas as gpd
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"data/processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Define county boundaries (simplified for this example)
COUNTIES = {
    "San Francisco": {
        "id": "sf",
        "bounds": {
            "minlat": 37.7,
            "maxlat": 37.8,
            "minlon": -122.5,
            "maxlon": -122.3
        }
    },
    "Los Angeles": {
        "id": "la",
        "bounds": {
            "minlat": 33.7,
            "maxlat": 34.8,
            "minlon": -118.7,
            "maxlon": -117.7
        }
    }
}

def get_latest_file(directory, pattern):
    """Get the latest file matching the pattern in the directory."""
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def load_fire_data():
    """Load the latest fire data."""
    try:
        latest_file = get_latest_file("data/fire", "california_fires_*.csv")
        if not latest_file:
            logger.error("No fire data files found")
            return None
        
        logger.info(f"Loading fire data from {latest_file}")
        df = pd.read_csv(latest_file)
        logger.info(f"Loaded {len(df)} fire records")
        return df
    except Exception as e:
        logger.error(f"Error loading fire data: {str(e)}")
        return None

def load_weather_data():
    """Load and combine weather data."""
    try:
        weather_files = glob.glob("data/weather/*.csv")
        if not weather_files:
            logger.error("No weather data files found")
            return None
        
        logger.info(f"Loading weather data from {len(weather_files)} files")
        dfs = []
        for file in weather_files:
            df = pd.read_csv(file)
            dfs.append(df)
        
        if not dfs:
            return None
        
        # Combine all weather dataframes
        combined_df = pd.concat(dfs, ignore_index=True)
        logger.info(f"Loaded {len(combined_df)} weather records")
        return combined_df
    except Exception as e:
        logger.error(f"Error loading weather data: {str(e)}")
        return None

def load_vegetation_data():
    """Load the latest vegetation data."""
    try:
        latest_file = get_latest_file("data/vegetation", "*_ndvi.csv")
        if not latest_file:
            logger.error("No vegetation data files found")
            return None
        
        logger.info(f"Loading vegetation data from {latest_file}")
        df = pd.read_csv(latest_file)
        logger.info(f"Loaded {len(df)} vegetation records")
        return df
    except Exception as e:
        logger.error(f"Error loading vegetation data: {str(e)}")
        return None

def assign_to_county(lat, lon):
    """Assign a coordinate to a county."""
    for county_name, county_info in COUNTIES.items():
        bounds = county_info["bounds"]
        if (bounds["minlat"] <= lat <= bounds["maxlat"] and 
            bounds["minlon"] <= lon <= bounds["maxlon"]):
            return county_info["id"]
    return None

def process_data_by_county():
    """Process data and organize by county."""
    # Load all data
    fire_df = load_fire_data()
    weather_df = load_weather_data()
    vegetation_df = load_vegetation_data()
    
    if fire_df is None or weather_df is None or vegetation_df is None:
        logger.error("Missing required data, cannot proceed")
        return False
    
    # Process for each county
    county_data = {}
    
    for county_name, county_info in COUNTIES.items():
        county_id = county_info["id"]
        bounds = county_info["bounds"]
        logger.info(f"Processing data for {county_name} county")
        
        # Filter fire data for this county
        county_fire_df = fire_df[
            (fire_df['latitude'] >= bounds["minlat"]) & 
            (fire_df['latitude'] <= bounds["maxlat"]) & 
            (fire_df['longitude'] >= bounds["minlon"]) & 
            (fire_df['longitude'] <= bounds["maxlon"])
        ].copy()
        
        # Count recent fires
        recent_fires = len(county_fire_df)
        
        # Calculate average fire radiative power
        avg_frp = county_fire_df['frp'].mean() if not county_fire_df.empty else 0
        
        # Get weather data for this county (simplified)
        # In a real implementation, you would match weather stations to the county
        county_weather = {
            "temperature": weather_df['TAVG'].mean() if 'TAVG' in weather_df.columns else 70,
            "humidity": weather_df['RHAVG'].mean() if 'RHAVG' in weather_df.columns else 50,
            "windSpeed": weather_df['AWND'].mean() if 'AWND' in weather_df.columns else 5,
            "windDirection": "NW"  # Simplified
        }
        
        # Get vegetation data (NDVI) for this county
        # In a real implementation, you would match NDVI values to the county
        county_ndvi = vegetation_df['ndvi'].mean() if 'ndvi' in vegetation_df.columns else 0.5
        
        # Calculate a suitability score based on all factors
        # This is a simplified example - in reality, you would use a more complex model
        suitability_score = calculate_suitability_score(
            recent_fires,
            avg_frp,
            county_weather["temperature"],
            county_weather["humidity"],
            county_weather["windSpeed"],
            county_ndvi
        )
        
        # Determine hazard proximity (simplified)
        hazard_proximity = "Low" if suitability_score > 80 else "Medium" if suitability_score > 60 else "High"
        
        # Create county data structure
        county_data[county_id] = {
            "id": county_id,
            "name": county_name,
            "coordinates": f"{(bounds['minlat'] + bounds['maxlat'])/2}, {(bounds['minlon'] + bounds['maxlon'])/2}",
            "score": int(suitability_score * 0.7),  # General risk score (lower is better)
            "riskLevel": "Low" if suitability_score > 80 else "Moderate" if suitability_score > 60 else "High",
            "riskColor": "green" if suitability_score > 80 else "yellow" if suitability_score > 60 else "red",
            "recentFires": recent_fires,
            "heatMW": int(avg_frp),
            "firmsScore": int(100 - suitability_score * 0.5),  # FIRMS score (lower is better)
            "historicalAvg": f"{max(1, int(recent_fires * 0.8))} fires/week",  # Simplified
            "historicalScore": int(100 - suitability_score * 0.6),  # Historical score (lower is better)
            "suitabilityScore": int(suitability_score),
            "weatherConditions": county_weather,
            "hazardProximity": hazard_proximity,
            "firePersonnel": 15 if county_id == "sf" else 12,  # Simplified
            "equipmentStatus": "Ready",  # Simplified
            "permitStatus": "Approved" if county_id == "sf" else "Pending"  # Simplified
        }
        
        logger.info(f"Processed {county_name} county: Suitability Score = {suitability_score:.1f}")
    
    # Save the processed data
    save_processed_data(county_data)
    
    return True

def calculate_suitability_score(recent_fires, avg_frp, temperature, humidity, wind_speed, ndvi):
    """
    Calculate a suitability score for controlled burns based on various factors.
    Higher score = more suitable for controlled burns.
    """
    # Convert inputs to numpy arrays for vectorized operations
    factors = np.array([
        recent_fires,
        avg_frp,
        temperature,
        humidity,
        wind_speed,
        ndvi
    ])
    
    # Weights for each factor (sum to 1)
    weights = np.array([
        -0.2,  # More recent fires = less suitable
        -0.1,  # Higher FRP = less suitable
        -0.15,  # Higher temperature = less suitable
        0.25,  # Higher humidity = more suitable
        -0.2,  # Higher wind speed = less suitable
        0.1   # Higher NDVI (greener vegetation) = more suitable
    ])
    
    # Normalize factors to 0-1 range
    normalized_factors = np.array([
        min(1.0, recent_fires / 20),  # Normalize fires (cap at 20)
        min(1.0, avg_frp / 1000),     # Normalize FRP (cap at 1000)
        (temperature - 50) / 50,      # Normalize temp (50-100°F)
        humidity / 100,               # Normalize humidity (0-100%)
        wind_speed / 20,              # Normalize wind (0-20 mph)
        ndvi                          # NDVI already in 0-1 range
    ])
    
    # Calculate weighted sum
    weighted_sum = np.sum(normalized_factors * weights)
    
    # Convert to 0-100 scale
    base_score = 50  # Start at middle
    score = base_score + (weighted_sum * 50)
    
    # Ensure score is in 0-100 range
    score = max(0, min(100, score))
    
    return score

def save_processed_data(county_data):
    """Save the processed data to CSV files."""
    try:
        # Create output directory
        os.makedirs("data/processed", exist_ok=True)
        
        # Save each county's data
        for county_id, data in county_data.items():
            # Create a flattened version of the data for CSV
            flat_data = data.copy()
            
            # Handle nested dictionaries
            if "weatherConditions" in flat_data:
                for key, value in flat_data["weatherConditions"].items():
                    flat_data[f"weather_{key}"] = value
                del flat_data["weatherConditions"]
            
            # Convert to DataFrame
            df = pd.DataFrame([flat_data])
            
            # Save to CSV
            output_file = os.path.join("data/processed", f"{county_id}_processed.csv")
            df.to_csv(output_file, index=False)
            logger.info(f"Saved processed data for {county_id} to {output_file}")
        
        # Save a combined file with all counties
        combined_df = pd.DataFrame([data for data in county_data.values()])
        combined_file = os.path.join("data/processed", "all_counties.csv")
        combined_df.to_csv(combined_file, index=False)
        logger.info(f"Saved combined data to {combined_file}")
        
        return True
    except Exception as e:
        logger.error(f"Error saving processed data: {str(e)}")
        return False

def main():
    """Run the data processing pipeline."""
    logger.info("Starting BurnAI data processing...")
    
    # Process data by county
    success = process_data_by_county()
    
    if success:
        logger.info("Data processing completed successfully")
    else:
        logger.error("Data processing failed")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 