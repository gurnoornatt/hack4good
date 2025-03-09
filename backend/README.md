# BurnAI Backend

This is the backend for the BurnAI Wildfire Risk & Controlled Burn Assessment application. It collects data from various sources, processes it, and uses AI to generate burn assessments.

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
├── collect_data.py        # Data collection script
├── process_data.py        # Data processing script
├── ai_analysis.py         # AI analysis script
├── run_pipeline.py        # Pipeline runner
└── requirements.txt       # Python dependencies
```

## Prerequisites

- Python 3.9+
- Google Earth Engine account
- NOAA API key
- OpenAI API key
- Google Drive API credentials

## Installation

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

## Usage

### Running the Full Pipeline

To run the entire pipeline (data collection, processing, AI analysis, and API server):

```bash
python run_pipeline.py
```

### Running Individual Components

#### 1. Data Collection

```bash
python collect_data.py
```

This will:
- Fetch fire data from NASA FIRMS
- Fetch weather data from NOAA
- Calculate vegetation indices using Google Earth Engine

#### 2. Data Processing

```bash
python process_data.py
```

This will:
- Process the collected data
- Calculate suitability scores
- Save processed data to CSV files

#### 3. AI Analysis

```bash
python ai_analysis.py
```

This will:
- Generate burn assessments using OpenAI
- Save assessments to JSON files

#### 4. API Server

```bash
cd api
python main.py
```

This will:
- Start the FastAPI server
- Expose the processed data and AI assessments through API endpoints

## API Endpoints

The API provides the following endpoints:

- `GET /api/counties` - Get list of all counties with basic data
- `GET /api/counties/{county_id}` - Get detailed data for a specific county
- `GET /api/weather/{county_id}` - Get current weather conditions for a county
- `GET /api/burn-assessment/{county_id}` - Get burn assessment for a county
- `GET /api/burn-assessment/export/{county_id}` - Generate and download assessment report
- `POST /api/burn-protocol/initiate` - Initiate burn protocol workflow
- `GET /api/fire-points/{county_id}` - Get recent fire points for a county
- `GET /api/historical-hotspots/{county_id}` - Get historical hotspots for a county
- `GET /api/map/counties` - Get GeoJSON data for county boundaries

## Data Sources

1. **NASA FIRMS**: Fire Information for Resource Management System
   - Provides active fire data
   - API Key: Not required for CSV downloads

2. **NOAA**: National Oceanic and Atmospheric Administration
   - Provides weather data
   - API Key: Required, get from https://www.ncdc.noaa.gov/cdo-web/token

3. **Google Earth Engine**: For vegetation indices
   - Provides NDVI (Normalized Difference Vegetation Index)
   - Authentication: Required, use `earthengine authenticate`

## Troubleshooting

### Common Issues

1. **API Rate Limits**:
   - NOAA and NASA APIs have rate limits
   - The code includes retry logic with exponential backoff

2. **Google Earth Engine**:
   - If authentication fails, run `earthengine authenticate`
   - Check for quota limits

3. **Data Processing**:
   - If data files are missing, check the data collection logs
   - Ensure all required directories exist

## Documentation

For more detailed information, see:

- [Technical Guide](docs/technical_guide.md) - Comprehensive guide for the backend
- [UI/UX Component Integration Guide](../docs/ui-integration-guide.md) - Guide for frontend integration