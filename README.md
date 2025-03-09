# BurnAI - Wildfire Risk & Controlled Burn Assessment

BurnAI is a professional platform that combines satellite data, weather patterns, and historical fire records to provide real-time wildfire risk assessment and controlled burn planning for California.

![BurnAI Dashboard](https://via.placeholder.com/800x400?text=BurnAI+Dashboard)

## Features

- **Real-time Wildfire Risk Analysis**: County-level risk scores updated daily with detailed breakdowns
- **Controlled Burn Assessment**: AI-powered recommendations for preventative controlled burns
- **Weather Integration**: Current and forecasted weather conditions for informed decision-making
- **Interactive Mapping**: Visualize risk zones, active fires, and historical hotspots
- **Resource Management**: Track fire personnel and equipment readiness
- **Dark Mode Support**: Comfortable viewing in all lighting conditions

## Getting Started

### Prerequisites

- Node.js 18.0.0 or higher
- npm 9.0.0 or higher

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/burnaisfla.git
   cd burnaisfla
   ```

2. Install dependencies
   ```bash
   npm install
   ```

3. Run the development server
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

- `app/` - Next.js application routes
  - `page.tsx` - Landing page
  - `dashboard/page.tsx` - Dashboard application
- `components/` - Reusable UI components
- `lib/` - Utility functions and shared code
- `public/` - Static assets
- `docs/` - Documentation

## Documentation

- [UI/UX Component Integration Guide](docs/ui-integration-guide.md) - Comprehensive guide for backend integration

## Technology Stack

- **Frontend**: Next.js 15, React 19, Tailwind CSS
- **UI Components**: shadcn/ui
- **State Management**: React Hooks
- **Styling**: Tailwind CSS with dark mode support
- **Icons**: Lucide React

## Development Workflow

1. Create a feature branch from `main`
2. Implement your changes
3. Submit a pull request
4. Ensure CI tests pass
5. Request a code review

## Backend Integration

This repository contains the frontend application. For backend integration, refer to the [UI/UX Component Integration Guide](docs/ui-integration-guide.md) which provides:

- Detailed component documentation
- Data model specifications
- API endpoint requirements
- Integration process guidelines

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- California Department of Forestry and Fire Protection
- NASA FIRMS (Fire Information for Resource Management System)
- National Weather Service
