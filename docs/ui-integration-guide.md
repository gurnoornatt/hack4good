# BurnAI UI/UX Component Integration Guide

This document provides a comprehensive overview of all UI components in the BurnAI application, their data dependencies, and integration points for backend development. This guide will ensure a seamless integration process between the frontend and backend systems.

## 1. Application Structure

The application consists of two main sections:
- **Landing Page** (`app/page.tsx`): Marketing and information page
- **Dashboard** (`app/dashboard/page.tsx`): Main application for controlled burn assessment

## 2. Theme System

The application supports both light and dark modes through a theme provider.

| Component | File Path | Description | Backend Integration Points |
|-----------|-----------|-------------|----------------------------|
| ThemeProvider | `components/theme-provider.tsx` | Manages theme state | No backend integration required |
| ThemeToggle | `components/ui/theme-toggle.tsx` | UI for toggling themes | No backend integration required |

## 3. Dashboard Components

### 3.1 Header Section

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| Header Title | None | None |
| Date Selector | Current date | Optional: Sync with backend for historical data retrieval |
| Refresh Button | `isRefreshing` state | API call to refresh all data from backend |

```typescript
// Integration example for refresh functionality
const handleRefresh = async () => {
  setIsRefreshing(true);
  try {
    // Backend API call
    const data = await fetchDashboardData(selectedCounty.id, date);
    // Update state with fresh data
    updateDashboardData(data);
  } catch (error) {
    // Handle error
  } finally {
    setIsRefreshing(false);
  }
};
```

### 3.2 County Selection Panel

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| County Cards | `countyData` array | API endpoint to fetch all counties with basic data |
| County Selection | `selectedCounty` state | API endpoint to fetch detailed data for selected county |
| Burn Suitability Bar | `suitabilityScore` | Calculate on backend based on multiple factors |
| Permit Status Badge | `permitStatus` | Fetch from permit management system |

```typescript
// Data structure for county list
interface CountyBasicData {
  id: string;
  name: string;
  coordinates: string;
  suitabilityScore: number;
  permitStatus: "Approved" | "Pending" | "Denied";
}

// API endpoint: GET /api/counties
```

### 3.3 Current Conditions Panel

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| Temperature | `weatherConditions.temperature` | Weather API integration |
| Humidity | `weatherConditions.humidity` | Weather API integration |
| Wind Speed | `weatherConditions.windSpeed` | Weather API integration |
| Wind Direction | `weatherConditions.windDirection` | Weather API integration |

```typescript
// Weather data structure
interface WeatherConditions {
  temperature: number; // in Fahrenheit
  humidity: number; // percentage
  windSpeed: number; // mph
  windDirection: string; // compass direction (N, NE, E, etc.)
  timestamp: string; // ISO date string of last update
}

// API endpoint: GET /api/weather/{countyId}
```

### 3.4 Burn Readiness Panel

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| Hazard Proximity | `hazardProximity` | GIS system integration to calculate proximity to hazards |
| Fire Personnel | `firePersonnel` | Resource management system integration |
| Equipment Status | `equipmentStatus` | Resource management system integration |

```typescript
// Burn readiness data structure
interface BurnReadiness {
  hazardProximity: "Low" | "Medium" | "High";
  firePersonnel: number;
  equipmentStatus: "Ready" | "Partial" | "Unavailable";
  lastUpdated: string; // ISO date string
}

// API endpoint: GET /api/burn-readiness/{countyId}
```

### 3.5 Map Component

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| Base Map | Map tiles | GIS service integration |
| County Overlays | County boundaries with color coding | GIS data for county boundaries |
| Fire Points | `showFirePoints` toggle, fire location data | Fire incident database integration |
| Historical Hotspots | `showHistorical` toggle, historical data | Historical fire database integration |
| Map Controls | None | None |

```typescript
// Fire point data structure
interface FirePoint {
  id: string;
  latitude: number;
  longitude: number;
  intensity: number; // Used for visualization
  timestamp: string; // ISO date string
}

// API endpoints:
// GET /api/fire-points/{countyId}
// GET /api/historical-hotspots/{countyId}?startDate={date}&endDate={date}
```

### 3.6 Burn Assessment Summary

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| Suitability Score | `suitabilityScore` | AI model for calculating suitability |
| Suitability Status Badge | Based on `suitabilityScore` | Derived from suitability score |
| Potential Limitations | `burnLimitations` array | AI analysis of limitations |
| Recommendations | `burnRecommendations` array | AI-generated recommendations |
| Export Button | None | Generate and download assessment report |
| Initiate Burn Protocol Button | Enabled based on `suitabilityScore` | Trigger burn protocol workflow |

```typescript
// Burn assessment data structure
interface BurnAssessment {
  suitabilityScore: number;
  suitabilityStatus: "Highly Suitable" | "Suitable with Caution" | "Not Recommended";
  limitations: {
    title: string;
    description: string;
  }[];
  recommendations: string[];
}

// API endpoints:
// GET /api/burn-assessment/{countyId}
// POST /api/burn-protocol/initiate
// GET /api/burn-assessment/export/{countyId}
```

### 3.7 Summary Stats Cards

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| Burn Suitability Card | `suitabilityScore` | AI model for calculating suitability |
| Hazard Proximity Card | `hazardProximity` | GIS system integration |
| Readiness Status Card | `permitStatus`, `firePersonnel`, `equipmentStatus` | Multiple system integrations |

## 4. Landing Page Components

### 4.1 Header Section

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| Navigation Links | None | None |
| Dashboard Button | None | None |
| ThemeToggle | Theme state | None |

### 4.2 Hero Section

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| Hero Content | None | None |
| CTA Buttons | None | None |
| County Preview Card | Sample county data | Optional: Fetch real-time sample data |

### 4.3 Features Section

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| Feature Cards | Feature data array | None (static content) |

### 4.4 Technology Section

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| Technology Items | Technology data array | None (static content) |
| Stats Cards | Stats data | Optional: Fetch real system stats |

### 4.5 Testimonials Section

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| Testimonial Cards | Testimonial data array | Optional: CMS integration for testimonials |

### 4.6 Pricing Section

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| Pricing Cards | Pricing data array | Optional: Pricing API integration |

### 4.7 CTA Section

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| CTA Buttons | None | None |

### 4.8 Footer Section

| Component | Data Dependencies | Backend Integration Points |
|-----------|-------------------|----------------------------|
| Footer Links | None | None |
| Social Links | None | None |

## 5. Data Models

### 5.1 County Data Model

```typescript
interface County {
  id: string;
  name: string;
  coordinates: string; // Format: "lat, long"
  score: number; // General risk score
  riskLevel: string;
  riskColor: string;
  recentFires: number;
  heatMW: number;
  firmsScore: number;
  historicalAvg: string;
  historicalScore: number;
  burnSuggestion: string;
  suitabilityScore: number;
  weatherConditions: WeatherConditions;
  hazardProximity: "Low" | "Medium" | "High";
  firePersonnel: number;
  equipmentStatus: "Ready" | "Partial" | "Unavailable";
  permitStatus: "Approved" | "Pending" | "Denied";
}

interface WeatherConditions {
  temperature: number;
  humidity: number;
  windSpeed: number;
  windDirection: string;
}
```

### 5.2 Burn Assessment Data Model

```typescript
interface BurnLimitation {
  title: string;
  description: string;
}

type BurnRecommendation = string;

interface BurnAssessment {
  countyId: string;
  suitabilityScore: number;
  limitations: BurnLimitation[];
  recommendations: BurnRecommendation[];
  assessmentDate: string; // ISO date string
}
```

## 6. API Endpoints

### 6.1 County Data

- `GET /api/counties` - Get list of all counties with basic data
- `GET /api/counties/{countyId}` - Get detailed data for a specific county

### 6.2 Weather Data

- `GET /api/weather/{countyId}` - Get current weather conditions for a county
- `GET /api/weather/{countyId}/forecast` - Get weather forecast for a county

### 6.3 Burn Assessment

- `GET /api/burn-assessment/{countyId}` - Get burn assessment for a county
- `GET /api/burn-assessment/export/{countyId}` - Generate and download assessment report
- `POST /api/burn-protocol/initiate` - Initiate burn protocol workflow

### 6.4 Map Data

- `GET /api/map/counties` - Get GeoJSON data for county boundaries
- `GET /api/fire-points/{countyId}` - Get recent fire points for a county
- `GET /api/historical-hotspots/{countyId}` - Get historical hotspots for a county

## 7. State Management

### 7.1 Global State

- Theme state (light/dark mode)
- User authentication state (if applicable)

### 7.2 Dashboard State

- Selected county
- Selected date
- Map display options (fire points, historical hotspots)
- Refresh state

## 8. Integration Process

1. **Backend API Development**:
   - Implement API endpoints following the structure outlined in this document
   - Ensure proper error handling and response formats
   - Implement data validation

2. **Frontend Integration**:
   - Replace mock data with API calls
   - Implement loading states for async operations
   - Add error handling for failed API calls

3. **Testing**:
   - Unit test individual components
   - Integration test API endpoints
   - End-to-end test complete workflows

4. **Deployment**:
   - Deploy backend services
   - Deploy frontend application
   - Configure environment variables

## 9. Authentication & Authorization

If the application requires authentication:

- Implement JWT-based authentication
- Define user roles and permissions
- Secure API endpoints based on user roles
- Implement session management

## 10. Performance Considerations

- Implement caching for frequently accessed data
- Optimize map rendering for large datasets
- Implement pagination for large data lists
- Use code splitting to reduce initial load time

## 11. Accessibility

- Ensure proper contrast ratios for all UI elements
- Add ARIA labels to interactive elements
- Ensure keyboard navigation works correctly
- Test with screen readers

## 12. Responsive Design

- Ensure all components work on mobile devices
- Implement responsive layouts for different screen sizes
- Test on various devices and browsers 