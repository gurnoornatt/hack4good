#!/usr/bin/env python3
"""
BurnAI API Server

This is the main entry point for the BurnAI API, which provides access to
processed data and AI assessments for wildfire risk and controlled burn planning.
"""
import os
import sys
import logging
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

# Import routes
from api.routes.counties import router as counties_router
from api.routes.data import router as data_router

# Import utils
from api.utils.logging import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging("burnai_api", os.getenv("LOG_LEVEL", "INFO"))

# Create FastAPI app
app = FastAPI(
    title="BurnAI API",
    description="API for BurnAI Wildfire Risk & Controlled Burn Assessment",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development server
        "https://burnaisfla.vercel.app",  # Production deployment
        "*",  # Allow all origins in development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(counties_router, prefix="/api")
app.include_router(data_router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {
        "message": "Welcome to the BurnAI API",
        "version": "1.0.0",
        "documentation": "/docs",
        "timestamp": datetime.now().isoformat(),
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Handle HTTP exceptions.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "path": request.url.path,
            "timestamp": datetime.now().isoformat(),
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Handle general exceptions.
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "status_code": 500,
            "path": request.url.path,
            "timestamp": datetime.now().isoformat(),
        },
    )

# Run the application
if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    logger.info(f"Starting BurnAI API server on {host}:{port} (debug={debug})")
    
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info",
    ) 