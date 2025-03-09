# BurnAI API

This is the API component of the BurnAI backend, which provides access to processed data and AI assessments for wildfire risk and controlled burn planning.

## Directory Structure

```
api/
├── models/            # Pydantic models for data validation
│   ├── __init__.py
│   └── schemas.py
├── routes/            # API route definitions
│   ├── __init__.py
│   ├── counties.py
│   └── data.py
├── utils/             # Utility functions
│   ├── __init__.py
│   └── logging.py
├── main.py            # Main FastAPI application
└── README.md          # This file
```

## API Endpoints

### Root Endpoints

- `GET /` - Welcome message and API information
- `GET /health` - Health check endpoint

### County Endpoints

- `GET /api/counties` - Get list of all counties with basic data
- `GET /api/counties/{county_id}` - Get detailed data for a specific county
- `GET /api/counties/{county_id}/assessment` - Get burn assessment for a specific county

### Data Endpoints

- `GET /api/data/fire-points/{county_id}` - Get recent fire points for a county
- `GET /api/data/weather/{county_id}` - Get current weather conditions for a county
- `GET /api/data/vegetation/{county_id}` - Get vegetation data for a county
- `POST /api/data/refresh` - Refresh all data by running collection, processing, and AI analysis

## Running the API

The API can be run using the `run_api.py` script in the parent directory:

```bash
python run_api.py
```

Or directly using Uvicorn:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Testing the API

The API can be tested using the `test_api.py` script in the parent directory:

```bash
python test_api.py
```

## API Documentation

Once the API is running, you can access the auto-generated documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 