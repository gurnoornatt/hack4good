#!/usr/bin/env python3
"""
BurnAI Data Collection Script

This script runs all data collection processes and generates CSV files
for fire data, weather data, and vegetation data.
"""

import os
import sys
import logging
import time
from datetime import datetime
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"data/collection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def create_data_directories():
    """Create necessary data directories if they don't exist."""
    directories = [
        "data",
        "data/weather",
        "data/fire",
        "data/vegetation",
        "data/processed"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")

def collect_nasa_firms_data():
    """Collect fire data from NASA FIRMS."""
    try:
        logger.info("Starting NASA FIRMS data collection...")
        from nasa_firms import FirmsAPI
        
        firms = FirmsAPI()
        df = firms.get_california_fires(total_days=30)
        
        if df is not None:
            logger.info(f"Successfully collected {len(df)} fire records")
            # Move the file to the fire directory
            latest_file = max([f for f in os.listdir("data") if f.startswith("california_fires_")], key=os.path.getctime)
            os.rename(os.path.join("data", latest_file), os.path.join("data/fire", latest_file))
            logger.info(f"Moved {latest_file} to data/fire directory")
            return True
        else:
            logger.error("Failed to collect NASA FIRMS data")
            return False
    except Exception as e:
        logger.error(f"Error in NASA FIRMS data collection: {str(e)}")
        return False

def collect_noaa_weather_data():
    """Collect weather data from NOAA."""
    try:
        logger.info("Starting NOAA weather data collection...")
        from noaa import NOAADataFetcher
        
        if not os.getenv('NOAA_API_KEY'):
            logger.error("NOAA_API_KEY environment variable not set")
            return False
        
        fetcher = NOAADataFetcher()
        fetcher.fetch_and_process()
        
        # Check if files were created
        weather_files = os.listdir("data/weather")
        if weather_files:
            logger.info(f"Successfully collected weather data: {len(weather_files)} files")
            return True
        else:
            logger.error("No weather data files were created")
            return False
    except Exception as e:
        logger.error(f"Error in NOAA weather data collection: {str(e)}")
        return False

def collect_vegetation_data():
    """Collect vegetation data using Google Earth Engine."""
    try:
        logger.info("Starting vegetation data collection...")
        
        # First, run the Earth Engine script to calculate NDVI and export to Google Drive
        logger.info("Calculating NDVI using Google Earth Engine...")
        import vegetation
        
        # Wait for the export to complete (this might take some time)
        logger.info("Waiting for Earth Engine export to complete...")
        time.sleep(60)  # Wait for 1 minute
        
        # Then, download and process the GeoTIFF file
        logger.info("Downloading and processing NDVI data...")
        import veg2
        
        # Check if the CSV file was created
        veg_files = [f for f in os.listdir("data") if f.endswith("_ndvi.csv")]
        if veg_files:
            # Move the file to the vegetation directory
            latest_file = max(veg_files, key=lambda f: os.path.getctime(os.path.join("data", f)))
            os.rename(os.path.join("data", latest_file), os.path.join("data/vegetation", latest_file))
            logger.info(f"Successfully collected vegetation data: {latest_file}")
            return True
        else:
            logger.error("No vegetation data files were created")
            return False
    except Exception as e:
        logger.error(f"Error in vegetation data collection: {str(e)}")
        return False

def main():
    """Run all data collection processes."""
    logger.info("Starting BurnAI data collection process...")
    
    # Create data directories
    create_data_directories()
    
    # Collect data from each source
    results = {
        "NASA FIRMS": collect_nasa_firms_data(),
        "NOAA Weather": collect_noaa_weather_data(),
        "Vegetation": collect_vegetation_data()
    }
    
    # Log results
    logger.info("Data collection completed with the following results:")
    for source, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        logger.info(f"{source}: {status}")
    
    # Return success if all processes succeeded
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 