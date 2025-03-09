# BurnAI Backend Technical Guide

## Overview

This document provides technical guidance for the BurnAI backend system, which collects data from various sources, processes it, and uses AI to generate wildfire risk assessments and controlled burn recommendations.

## Architecture

The backend is structured as follows:

```
backend/
├── data/                  # Storage for CSV data files
├── models/                # ML models and AI integration
├── services/              # Data processing services
├── utils/                 # Utility functions
├── api/                   # FastAPI endpoints
├── notebooks/             # Jupyter notebooks for analysis
├── docs/                  # Documentation
├── nasa_firms.py          # NASA FIRMS fire data collection
├── noaa.py                # NOAA weather data collection
├── vegetation.py          # Earth Engine vegetation data (NDVI)
├── veg2.py                # Google Drive integration for vegetation data
└── requirements.txt       # Python dependencies
```

## Data Sources

1. **NASA FIRMS** (`nasa_firms.py`): 
   - Collects active fire data from NASA's Fire Information for Resource Management System
   - Provides latitude, longitude, acquisition date, and fire radiative power (FRP)
   - Outputs: `california_fires_YYYYMMDD.csv`

2. **NOAA Weather** (`noaa.py`):
   - Collects weather data for the San Francisco Bay Area
   - Provides temperature, precipitation, wind speed, wind direction, and humidity
   - Outputs: Weather data CSVs in `data/weather/`

3. **Vegetation Data** (`vegetation.py` and `veg2.py`):
   - Uses Google Earth Engine to calculate NDVI (Normalized Difference Vegetation Index)
   - Exports GeoTIFF files to Google Drive
   - Downloads and processes GeoTIFF files to CSV format
   - Outputs: NDVI data in CSV format

## Data Processing Workflow

1. **Data Collection**:
   - Run each data collection script to gather raw data
   - Store raw data in CSV format in the `data/` directory

2. **Data Processing**:
   - Clean and preprocess the raw data
   - Merge datasets based on geographic coordinates and time
   - Calculate derived metrics (e.g., fire risk scores)

3. **AI Integration**:
   - Feed processed data to AI models
   - Generate risk assessments and recommendations
   - Store AI outputs for API access

4. **API Exposure**:
   - Expose processed data and AI insights through FastAPI endpoints
   - Ensure compatibility with the Next.js frontend

## Environment Setup

### Prerequisites

- Python 3.9+
- Google Earth Engine account
- NOAA API key
- Google Drive API credentials

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file with the following variables:
     ```
     NOAA_API_KEY=your_noaa_api_key
     OPENAI_API_KEY=your_openai_api_key
     ```

4. Authenticate with Google Earth Engine:
   - Ensure `credentials.json` is present for Google Drive API
   - Run `earthengine authenticate` if using Earth Engine CLI

## Data Collection Process

### 1. NASA FIRMS Fire Data

```bash
python nasa_firms.py
```

This will:
- Fetch fire data for California for the last 30 days
- Save the data to `data/california_fires_YYYYMMDD.csv`

### 2. NOAA Weather Data

```bash
python noaa.py
```

This will:
- Fetch weather data for the San Francisco Bay Area
- Process and save the data to `data/weather/`

### 3. Vegetation Data

```bash
python vegetation.py
python veg2.py
```

This will:
- Calculate NDVI using Google Earth Engine
- Export GeoTIFF to Google Drive
- Download and process the GeoTIFF to CSV

## AI Integration

The AI component will:
1. Read all CSV data files
2. Apply complex equations and algorithms to assess fire risk
3. Generate suitability scores for controlled burns
4. Provide recommendations and limitations

## API Development

The FastAPI endpoints will be developed to match the requirements specified in the UI/UX Component Integration Guide, including:

- `/api/counties` - Get list of all counties with basic data
- `/api/counties/{countyId}` - Get detailed data for a specific county
- `/api/weather/{countyId}` - Get current weather conditions for a county
- `/api/burn-assessment/{countyId}` - Get burn assessment for a county

## Integration with Frontend

The backend will provide data in the format expected by the frontend, as specified in the UI/UX Component Integration Guide. This includes:

- County data with suitability scores
- Weather conditions
- Burn readiness information
- Fire points and historical hotspots
- AI-generated recommendations

## Troubleshooting

### Common Issues

1. **API Rate Limits**:
   - NOAA and NASA APIs have rate limits
   - Implement retry logic with exponential backoff

2. **Google Earth Engine**:
   - Ensure proper authentication
   - Check for quota limits

3. **Data Processing**:
   - Handle missing or inconsistent data
   - Implement robust error handling

## Next Steps

1. Complete data collection scripts
2. Implement data processing pipeline
3. Develop AI integration
4. Create FastAPI endpoints
5. Test integration with frontend 