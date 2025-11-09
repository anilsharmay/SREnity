import React, { useState } from 'react';
import type { Alert, Service, IncidentHistoryEntry } from '../types';
import AlertsSection from './AlertsSection';
import ServicesTable from './ServicesTable';
import Sidebar from './Sidebar';
import IncidentHistorySection from './IncidentHistorySection';

interface DashboardProps {
  alerts: Alert[];
  services: Service[];
  incidentHistory?: IncidentHistoryEntry[];
  onAnalyzeAlert: (alertId: string) => void;
  onAnalyzeService: (serviceId: string) => void;
  onServiceDetails?: (serviceId: string) => void;
  onAlertDetails?: (alertId: string) => void;
}

const Dashboard: React.FC<DashboardProps> = ({
  alerts,
  services,
  incidentHistory = [],
  onAnalyzeAlert,
  onAnalyzeService,
  onServiceDetails,
  onAlertDetails
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [environmentFilter, setEnvironmentFilter] = useState('production');
  const [timeWindow, setTimeWindow] = useState('15 minutes');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const filteredServices = services.filter(service => {
    const matchesSearch = service.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesEnv = service.environment === environmentFilter.toLowerCase();
    return matchesSearch && matchesEnv;
  });

  const handleAnalyzeAlert = (alertId: string) => {
    console.log('Analyze alert:', alertId);
    onAnalyzeAlert(alertId);
  };

  const handleAnalyzeService = (serviceId: string) => {
    console.log('Analyze service:', serviceId);
    onAnalyzeService(serviceId);
  };

  const handleServiceClick = (serviceId: string) => {
    console.log('Service details:', serviceId);
    if (onServiceDetails) {
      onServiceDetails(serviceId);
    }
  };

  const handleAlertDetails = (alertId: string) => {
    console.log('Alert details:', alertId);
    if (onAlertDetails) {
      onAlertDetails(alertId);
    }
  };

  return (
    <div className="dashboard-container">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      
      <div className="dashboard-header">
        <div className="header-left">
          <button 
            className="hamburger-button"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle menu"
          >
            ☰
          </button>
          <h1>ACME web app - App Health Dashboard</h1>
        </div>
        <div className="header-right">
          <label htmlFor="env-select" className="env-label">Env:</label>
          <select
            id="env-select"
            className="filter-select"
            value={environmentFilter}
            onChange={(e) => setEnvironmentFilter(e.target.value)}
          >
            <option value="production">Production</option>
            <option value="staging">Staging</option>
            <option value="development">Development</option>
          </select>
        </div>
      </div>

      <div className="dashboard-controls-row">
        <input
          type="text"
          className="search-input"
          placeholder="Search transactions, errors, and metrics..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <div className="time-window-group">
          <label htmlFor="time-window" className="time-window-label">Time Window:</label>
          <select
            id="time-window"
            className="time-window-select"
            value={timeWindow}
            onChange={(e) => setTimeWindow(e.target.value)}
          >
            <option value="15 minutes">Last 15 minutes</option>
            <option value="30 minutes">Last 30 minutes</option>
            <option value="1 hour">Last 1 hour</option>
            <option value="1 day">Last 1 day</option>
            <option value="1 week">Last 1 week</option>
          </select>
        </div>
      </div>

      <AlertsSection
        alerts={alerts}
        onAnalyze={handleAnalyzeAlert}
        onViewDetails={handleAlertDetails}
      />

      {incidentHistory.length > 0 && (
        <>
          <div className="section-divider" />
          <IncidentHistorySection incidents={incidentHistory} />
        </>
      )}

      {(alerts.length > 0 || incidentHistory.length > 0) && <div className="section-divider" />}

      <div className="section-header">
        <span>All Services</span>
      </div>

      <ServicesTable
        services={filteredServices}
        onServiceClick={handleServiceClick}
        onAnalyze={handleAnalyzeService}
        onViewDetails={onServiceDetails}
      />
    </div>
  );
};

export default Dashboard;

