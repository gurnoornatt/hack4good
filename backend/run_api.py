#!/usr/bin/env python3
"""
BurnAI API Server Runner

This script runs the BurnAI API server.
"""
import os
import sys
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Run the API server."""
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    print(f"Starting BurnAI API server on {host}:{port} (debug={debug})")
    
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info",
    )
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 