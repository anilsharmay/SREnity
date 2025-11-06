# SREnity Frontend - V0 Static UI

Dark mode dashboard for SREnity with Elastic APM-style services table.

## Features

- Dark mode theme
- Alert banner section (independent of services)
- Services table with metrics
- Sparkline graphs for trends
- Three-dot menu (⋮) for actions
- Mock data (no API calls)

## Development

```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build
```

## Component Structure

- `Dashboard.tsx` - Main dashboard container
- `AlertsSection.tsx` - Alert banner
- `ServicesTable.tsx` - Services table
- `ServiceRow.tsx` - Individual service row
- `AlertCard.tsx` - Individual alert card
- `ThreeDotMenu.tsx` - Actions menu (⋮)
- `Sparkline.tsx` - Trend graphs
- `StatusBadge.tsx` - Health indicators

## Next Steps

- Connect to FastAPI backend
- Add RCA + Runbook analysis results view
- Add service details view
- Add alert details view
