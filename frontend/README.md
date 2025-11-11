# SREnity Frontend

React-based dashboard for SREnity's incident analysis and monitoring interface.

## Overview

Modern, responsive frontend application that provides a real-time dashboard for monitoring services and alerts, with integrated SREnity analysis capabilities.

## Features

- **Dashboard**: Service health monitoring with metrics and alerts
- **Real-Time Analysis**: Streaming analysis results via Server-Sent Events (SSE)
- **Progress Tracking**: Visual timeline showing analysis progress
- **RCA Display**: Structured root cause analysis with evidence and recommendations
- **Runbook Integration**: Direct links to relevant remediation procedures
- **Dark Theme**: Modern, polished UI with gradients and animations

## Setup

1. **Install dependencies**:
```bash
npm install
```

2. **Run development server**:
```bash
npm run dev
```

3. **Build for production**:
```bash
npm run build
```

## Architecture

### Components

- **Dashboard.tsx**: Main dashboard container with services table and alerts
- **AnalysisView.tsx**: Full-screen analysis results view with progress timeline
- **AlertsSection.tsx**: Active alerts display
- **ServicesTable.tsx**: Services table with metrics and status
- **ServiceRow.tsx**: Individual service row with sparklines
- **StatusBadge.tsx**: Health status indicators

### Hooks

- **useAnalysisStream.ts**: Custom hook for managing SSE connection to backend analysis endpoint

### Styling

- **globals.css**: Global CSS variables and base styles
- **dashboard.css**: Dashboard-specific styles
- **analysis.css**: Analysis view styles

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000`:

- **POST /api/analyze/stream**: Streaming analysis endpoint
- Uses Server-Sent Events (SSE) for real-time updates
- Handles status messages, RCA results, and runbook recommendations

## Key Features

### Dashboard
- Service health monitoring
- Alert management
- Environment filtering
- Time window selection
- Search functionality

### Analysis View
- Real-time progress timeline
- Root cause analysis summary
- Evidence and recommendations
- Runbook links
- Status log (collapsible)

## Development

The frontend is built with:
- **React 18+**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **CSS Modules**: Component styling

## Environment Configuration

The frontend expects the backend to be running on `http://localhost:8000`. To change this, update the API URL in `src/hooks/useAnalysisStream.ts`.
