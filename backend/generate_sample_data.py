#!/usr/bin/env python3
"""
BurnAI Sample Data Generator

This script generates sample data for testing the BurnAI API.
"""
import os
import sys
import json
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

def create_directories():
    """Create necessary directories for sample data."""
    directories = [
        "data/raw/nasa",
        "data/raw/noaa",
        "data/raw/vegetation",
        "data/processed",
        "data/assessments"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("Created directories for sample data")

def generate_fire_data():
    """Generate sample fire data."""
    print("Generating sample fire data...")
    
    # Define county boundaries
    counties = {
        "sf": {
            "name": "San Francisco",
            "bounds": {
                "min_lat": 37.7,
                "max_lat": 37.8,
                "min_lon": -122.5,
                "max_lon": -122.3
            }
        },
        "la": {
            "name": "Los Angeles",
            "bounds": {
                "min_lat": 33.7,
                "max_lat": 34.8,
                "min_lon": -118.7,
                "max_lon": -117.7
            }
        }
    }
    
    # Generate fire points
    fire_points = []
    
    for county_id, county in counties.items():
        # Generate 10-20 fire points per county
        num_points = random.randint(10, 20)
        
        for i in range(num_points):
            # Random date in the last 30 days
            date = datetime.now() - timedelta(days=random.randint(0, 30))
            
            # Random location within county bounds
            lat = random.uniform(county["bounds"]["min_lat"], county["bounds"]["max_lat"])
            lon = random.uniform(county["bounds"]["min_lon"], county["bounds"]["max_lon"])
            
            # Random fire radiative power (FRP)
            frp = random.uniform(0.1, 10.0)
            
            fire_points.append({
                "county_id": county_id,
                "latitude": lat,
                "longitude": lon,
                "acquisition_date": date.strftime("%Y-%m-%d"),
                "acquisition_time": date.strftime("%H:%M:%S"),
                "frp": frp,
                "confidence": random.randint(0, 100)
            })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(fire_points)
    filename = f"data/raw/nasa/california_fires_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    
    print(f"Generated {len(fire_points)} fire points and saved to {filename}")

def generate_weather_data():
    """Generate sample weather data."""
    print("Generating sample weather data...")
    
    # Define counties
    counties = ["sf", "la"]
    
    # Generate weather data for the last 30 days
    weather_data = []
    
    for county_id in counties:
        for day in range(30):
            date = datetime.now() - timedelta(days=day)
            
            # Random weather conditions
            temperature = random.uniform(15.0, 30.0)  # Celsius
            humidity = random.uniform(30.0, 80.0)  # Percentage
            wind_speed = random.uniform(0.0, 20.0)  # km/h
            precipitation = random.uniform(0.0, 10.0)  # mm
            
            weather_data.append({
                "county_id": county_id,
                "date": date.strftime("%Y-%m-%d"),
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "precipitation": precipitation
            })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(weather_data)
    filename = f"data/raw/noaa/weather_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    
    print(f"Generated {len(weather_data)} weather records and saved to {filename}")

def generate_vegetation_data():
    """Generate sample vegetation data."""
    print("Generating sample vegetation data...")
    
    # Define counties
    counties = ["sf", "la"]
    
    # Generate vegetation data
    vegetation_data = []
    
    for county_id in counties:
        # Generate 50-100 vegetation points per county
        num_points = random.randint(50, 100)
        
        for i in range(num_points):
            # Random NDVI value (Normalized Difference Vegetation Index)
            ndvi = random.uniform(0.0, 1.0)
            
            # Vegetation density based on NDVI
            vegetation_density = ndvi * 0.8 + random.uniform(0.0, 0.2)
            
            # Vegetation type based on NDVI
            if ndvi < 0.2:
                vegetation_type = "barren"
            elif ndvi < 0.4:
                vegetation_type = "sparse"
            elif ndvi < 0.6:
                vegetation_type = "moderate"
            elif ndvi < 0.8:
                vegetation_type = "dense"
            else:
                vegetation_type = "very dense"
            
            vegetation_data.append({
                "county_id": county_id,
                "ndvi_value": ndvi,
                "vegetation_density": vegetation_density,
                "vegetation_type": vegetation_type
            })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(vegetation_data)
    filename = f"data/raw/vegetation/vegetation_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    
    print(f"Generated {len(vegetation_data)} vegetation records and saved to {filename}")

def generate_processed_data():
    """Generate sample processed data."""
    print("Generating sample processed data...")
    
    # Define counties
    counties = {
        "sf": {
            "name": "San Francisco",
            "state": "California",
            "coordinates": {"lat": 37.7749, "lon": -122.4194}
        },
        "la": {
            "name": "Los Angeles",
            "state": "California",
            "coordinates": {"lat": 34.0522, "lon": -118.2437}
        }
    }
    
    # Generate processed data for each county
    all_county_data = []
    
    for county_id, county_info in counties.items():
        # Generate random data
        recent_fires = random.randint(5, 20)
        avg_frp = random.uniform(1.0, 5.0)
        temperature = random.uniform(15.0, 30.0)
        humidity = random.uniform(30.0, 80.0)
        wind_speed = random.uniform(0.0, 20.0)
        precipitation = random.uniform(0.0, 10.0)
        ndvi = random.uniform(0.3, 0.8)
        vegetation_density = ndvi * 0.8 + random.uniform(0.0, 0.2)
        
        # Calculate suitability score
        fire_risk = 0.3 * recent_fires / 20 + 0.7 * avg_frp / 5
        weather_factor = (0.4 * (1 - humidity / 100) + 
                         0.3 * temperature / 30 + 
                         0.3 * wind_speed / 20)
        vegetation_factor = vegetation_density
        
        suitability_score = 100 * (1 - (0.4 * fire_risk + 
                                      0.3 * weather_factor + 
                                      0.3 * vegetation_factor))
        
        # Ensure score is between 0 and 100
        suitability_score = max(0, min(100, suitability_score))
        
        # Create county data
        county_data = {
            "county_id": county_id,
            "name": county_info["name"],
            "state": county_info["state"],
            "coordinates_lat": county_info["coordinates"]["lat"],
            "coordinates_lon": county_info["coordinates"]["lon"],
            "recent_fires": recent_fires,
            "avg_frp": avg_frp,
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "precipitation": precipitation,
            "ndvi": ndvi,
            "vegetation_density": vegetation_density,
            "fire_risk": fire_risk,
            "historical_fires": random.randint(50, 200),
            "suitability_score": suitability_score
        }
        
        all_county_data.append(county_data)
        
        # Save individual county data
        df_county = pd.DataFrame([county_data])
        filename = f"data/processed/{county_id}_processed.csv"
        df_county.to_csv(filename, index=False)
        
        print(f"Generated processed data for {county_info['name']} and saved to {filename}")
    
    # Save combined data
    df_all = pd.DataFrame(all_county_data)
    filename = f"data/processed/combined_{datetime.now().strftime('%Y%m%d')}.csv"
    df_all.to_csv(filename, index=False)
    
    print(f"Generated combined processed data and saved to {filename}")

def generate_assessments():
    """Generate sample AI assessments."""
    print("Generating sample AI assessments...")
    
    # Define counties
    counties = {
        "sf": "San Francisco",
        "la": "Los Angeles"
    }
    
    for county_id, county_name in counties.items():
        # Generate random suitability score
        suitability_score = random.uniform(30.0, 90.0)
        
        # Determine overall recommendation based on score
        if suitability_score >= 70:
            overall_recommendation = "Highly suitable for controlled burns with proper precautions."
        elif suitability_score >= 50:
            overall_recommendation = "Suitable for controlled burns with additional precautions and monitoring."
        else:
            overall_recommendation = "Not recommended for controlled burns at this time due to high risk factors."
        
        # Generate key factors
        key_factors = [
            {
                "name": "Weather Conditions",
                "value": random.uniform(0.3, 0.8),
                "weight": 0.4
            },
            {
                "name": "Vegetation Density",
                "value": random.uniform(0.3, 0.8),
                "weight": 0.3
            },
            {
                "name": "Historical Fire Activity",
                "value": random.uniform(0.3, 0.8),
                "weight": 0.2
            },
            {
                "name": "Proximity to Populated Areas",
                "value": random.uniform(0.3, 0.8),
                "weight": 0.1
            }
        ]
        
        # Generate limitations
        limitations = [
            {
                "factor": "Weather",
                "description": "Current wind conditions may affect burn operations",
                "severity": "medium" if suitability_score < 70 else "low"
            },
            {
                "factor": "Vegetation",
                "description": "Dense vegetation in some areas requires careful management",
                "severity": "high" if random.random() < 0.3 else "medium"
            },
            {
                "factor": "Resources",
                "description": "Limited fire personnel availability for monitoring",
                "severity": "medium" if random.random() < 0.5 else "low"
            }
        ]
        
        # Generate recommendations
        recommendations = [
            "Conduct burns during early morning hours when humidity is higher",
            "Establish firebreaks around the perimeter of the burn area",
            "Notify local residents and businesses before conducting burns",
            "Have water resources readily available for containment if needed",
            "Monitor weather forecasts closely for changes in conditions"
        ]
        
        # Create assessment data
        assessment = {
            "county_id": county_id,
            "county_name": county_name,
            "timestamp": datetime.now().isoformat(),
            "overall_recommendation": overall_recommendation,
            "suitability_score": suitability_score,
            "key_factors": key_factors,
            "limitations": limitations,
            "recommendations": recommendations,
            "weather_impact": "Current weather conditions are generally favorable for controlled burns, but wind speeds should be monitored closely.",
            "vegetation_analysis": "Vegetation density varies across the county, with some areas requiring more careful management than others.",
            "historical_context": f"The {county_name} area has experienced {random.randint(5, 20)} wildfires in the past year, indicating moderate fire activity."
        }
        
        # Save assessment to JSON file
        filename = f"data/assessments/{county_id}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, "w") as f:
            json.dump(assessment, f, indent=2)
        
        print(f"Generated assessment for {county_name} and saved to {filename}")

def main():
    """Run the sample data generator."""
    print("=== BurnAI Sample Data Generator ===")
    
    # Create directories
    create_directories()
    
    # Generate sample data
    generate_fire_data()
    generate_weather_data()
    generate_vegetation_data()
    generate_processed_data()
    generate_assessments()
    
    print("\nSample data generation complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 