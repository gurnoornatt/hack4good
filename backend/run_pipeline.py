#!/usr/bin/env python3
"""
BurnAI Pipeline Runner

This script runs the entire BurnAI data pipeline:
1. Collect data from various sources
2. Process the data
3. Generate AI assessments
4. Start the API server
"""

import os
import sys
import logging
import subprocess
import time
from datetime import datetime
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"data/pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def run_script(script_name, description):
    """Run a Python script and return success status."""
    logger.info(f"Starting {description}...")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Log the output
        for line in result.stdout.splitlines():
            logger.info(f"{script_name}: {line}")
        
        logger.info(f"{description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"{description} failed with exit code {e.returncode}")
        
        # Log the error output
        for line in e.stderr.splitlines():
            logger.error(f"{script_name} error: {line}")
        
        return False
    except Exception as e:
        logger.error(f"Error running {description}: {str(e)}")
        return False

def run_api_server():
    """Start the API server."""
    logger.info("Starting API server...")
    
    try:
        # Change to the api directory
        os.chdir("api")
        
        # Start the server
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Change back to the original directory
        os.chdir("..")
        
        logger.info(f"API server started with PID {process.pid}")
        
        # Wait a moment to see if the server starts successfully
        time.sleep(2)
        
        if process.poll() is not None:
            # Server exited immediately
            stdout, stderr = process.communicate()
            logger.error(f"API server failed to start: {stderr}")
            return False
        
        logger.info("API server is running")
        return True
    except Exception as e:
        logger.error(f"Error starting API server: {str(e)}")
        return False

def main():
    """Run the entire pipeline."""
    logger.info("Starting BurnAI pipeline...")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Step 1: Collect data
    if not run_script("collect_data.py", "Data collection"):
        logger.error("Data collection failed, stopping pipeline")
        return False
    
    # Step 2: Process data
    if not run_script("process_data.py", "Data processing"):
        logger.error("Data processing failed, stopping pipeline")
        return False
    
    # Step 3: Generate AI assessments
    if not run_script("ai_analysis.py", "AI analysis"):
        logger.error("AI analysis failed, stopping pipeline")
        return False
    
    # Step 4: Start API server
    if not run_api_server():
        logger.error("API server failed to start, stopping pipeline")
        return False
    
    logger.info("BurnAI pipeline completed successfully")
    logger.info("API server is running. Press Ctrl+C to stop.")
    
    # Keep the script running while the API server is running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping BurnAI pipeline...")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 