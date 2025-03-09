#!/usr/bin/env python3
"""
BurnAI AI Analysis Script

This script uses OpenAI to analyze the processed data and generate
burn assessments, recommendations, and limitations.
"""

import os
import sys
import logging
import pandas as pd
import json
from datetime import datetime
import glob
from dotenv import load_dotenv
import openai
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"data/ai_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set up OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    logger.error("OPENAI_API_KEY environment variable not set")
    sys.exit(1)

def get_latest_file(directory, pattern):
    """Get the latest file matching the pattern in the directory."""
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def load_county_data(county_id):
    """Load the processed data for a specific county."""
    try:
        file_path = os.path.join("data/processed", f"{county_id}_processed.csv")
        if not os.path.exists(file_path):
            logger.error(f"No processed data file found for county {county_id}")
            return None
        
        logger.info(f"Loading processed data from {file_path}")
        df = pd.read_csv(file_path)
        if df.empty:
            logger.error(f"Empty data file for county {county_id}")
            return None
        
        # Convert DataFrame to dictionary
        county_data = df.iloc[0].to_dict()
        logger.info(f"Loaded processed data for {county_data.get('name', county_id)}")
        return county_data
    except Exception as e:
        logger.error(f"Error loading county data: {str(e)}")
        return None

def generate_burn_assessment(county_data):
    """
    Generate a burn assessment using OpenAI.
    
    Args:
        county_data: Dictionary containing processed county data
        
    Returns:
        Dictionary containing AI-generated assessment
    """
    try:
        # Extract relevant data for the prompt
        county_name = county_data.get("name", "Unknown")
        coordinates = county_data.get("coordinates", "Unknown")
        suitability_score = county_data.get("suitabilityScore", 0)
        recent_fires = county_data.get("recentFires", 0)
        temperature = county_data.get("weather_temperature", 70)
        humidity = county_data.get("weather_humidity", 50)
        wind_speed = county_data.get("weather_windSpeed", 5)
        wind_direction = county_data.get("weather_windDirection", "Unknown")
        hazard_proximity = county_data.get("hazardProximity", "Unknown")
        
        # Create the prompt
        prompt = f"""
        You are an expert wildfire analyst and controlled burn specialist. Analyze the following data for {county_name} County (coordinates: {coordinates}) and provide a detailed assessment for controlled burn suitability.

        DATA:
        - Suitability Score: {suitability_score}/100 (higher is better)
        - Recent Fires: {recent_fires} incidents
        - Temperature: {temperature}°F
        - Humidity: {humidity}%
        - Wind Speed: {wind_speed} mph
        - Wind Direction: {wind_direction}
        - Hazard Proximity: {hazard_proximity}

        Based on this data, provide:
        1. A brief assessment of the suitability for controlled burns (2-3 sentences)
        2. Three specific limitations or concerns
        3. Five specific recommendations for conducting a controlled burn safely
        
        Format your response as a JSON object with the following structure:
        {{
            "assessment": "Your assessment here...",
            "limitations": [
                {{"title": "Limitation 1 title", "description": "Limitation 1 description"}},
                {{"title": "Limitation 2 title", "description": "Limitation 2 description"}},
                {{"title": "Limitation 3 title", "description": "Limitation 3 description"}}
            ],
            "recommendations": [
                "Recommendation 1",
                "Recommendation 2",
                "Recommendation 3",
                "Recommendation 4",
                "Recommendation 5"
            ]
        }}
        """
        
        logger.info(f"Generating burn assessment for {county_name}")
        
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert wildfire analyst and controlled burn specialist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract and parse the response
        ai_response = response.choices[0].message.content.strip()
        assessment_data = json.loads(ai_response)
        
        logger.info(f"Successfully generated burn assessment for {county_name}")
        return assessment_data
    
    except Exception as e:
        logger.error(f"Error generating burn assessment: {str(e)}")
        
        # Return a default assessment in case of error
        return {
            "assessment": f"Unable to generate assessment for {county_data.get('name', 'Unknown')} due to an error.",
            "limitations": [
                {"title": "Data limitations", "description": "Assessment could not be generated due to data or API issues."}
            ],
            "recommendations": [
                "Please try again later or contact support."
            ]
        }

def save_assessment(county_id, assessment_data):
    """Save the AI-generated assessment to a JSON file."""
    try:
        # Create output directory
        os.makedirs("data/assessments", exist_ok=True)
        
        # Save to JSON file
        output_file = os.path.join("data/assessments", f"{county_id}_assessment.json")
        with open(output_file, 'w') as f:
            json.dump(assessment_data, f, indent=2)
        
        logger.info(f"Saved assessment for {county_id} to {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving assessment: {str(e)}")
        return False

def process_county(county_id):
    """Process a single county."""
    # Load county data
    county_data = load_county_data(county_id)
    if not county_data:
        return False
    
    # Generate burn assessment
    assessment = generate_burn_assessment(county_data)
    if not assessment:
        return False
    
    # Save assessment
    success = save_assessment(county_id, assessment)
    return success

def main():
    """Run the AI analysis for all counties."""
    logger.info("Starting BurnAI AI analysis...")
    
    # List of county IDs to process
    county_ids = ["sf", "la"]
    
    # Process each county
    results = {}
    for county_id in county_ids:
        logger.info(f"Processing county {county_id}")
        success = process_county(county_id)
        results[county_id] = success
    
    # Log results
    logger.info("AI analysis completed with the following results:")
    for county_id, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        logger.info(f"{county_id}: {status}")
    
    # Return success if all counties were processed successfully
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 