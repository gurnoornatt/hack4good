#!/usr/bin/env python3
"""
BurnAI API Documentation Checker

This script opens the API documentation in a web browser.
"""
import os
import sys
import webbrowser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Open the API documentation in a web browser."""
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "8000")
    
    # Use localhost instead of 0.0.0.0 for browser
    if host == "0.0.0.0":
        host = "localhost"
    
    # URLs for documentation
    swagger_url = f"http://{host}:{port}/docs"
    redoc_url = f"http://{host}:{port}/redoc"
    
    print(f"Opening Swagger UI at {swagger_url}")
    webbrowser.open(swagger_url)
    
    print(f"Opening ReDoc at {redoc_url}")
    webbrowser.open(redoc_url)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 