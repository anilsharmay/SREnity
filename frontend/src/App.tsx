import { useState } from 'react';
import Dashboard from './components/Dashboard';
import AnalysisView from './components/AnalysisView';
import { mockAlerts, mockServices, mockIncidentHistory } from './data/mockData';
import type { Alert, Service } from './types';
import './styles/globals.css';
import './styles/dashboard.css';

type View = 'dashboard' | 'analysis';

interface AnalysisContext {
  alert?: Alert;
  service?: Service;
  query: string;
}

function App() {
  const [currentView, setCurrentView] = useState<View>('dashboard');
  const [analysisContext, setAnalysisContext] = useState<AnalysisContext | null>(null);

  const handleAnalyzeAlert = (alertId: string) => {
    const alert = mockAlerts.find(a => a.id === alertId);
    if (!alert) {
      console.error('Alert not found:', alertId);
      return;
    }

    const query = `${alert.title}. ${alert.description || ''} Affects: ${alert.affects}`;
    setAnalysisContext({
      alert,
      query,
    });
    setCurrentView('analysis');
  };

  const handleAnalyzeService = (serviceId: string) => {
    const service = mockServices.find(s => s.id === serviceId);
    if (!service) {
      console.error('Service not found:', serviceId);
      return;
    }

    const query = `Analyze service ${service.name} in ${service.environment}. Status: ${service.status}`;
    setAnalysisContext({
      service,
      query,
    });
    setCurrentView('analysis');
  };

  const handleServiceDetails = (serviceId: string) => {
    console.log('Viewing service details:', serviceId);
    // TODO: Navigate to service details view
  };

  const handleAlertDetails = (alertId: string) => {
    console.log('Viewing alert details:', alertId);
    // TODO: Navigate to alert details view
  };

  const handleBackToDashboard = () => {
    setCurrentView('dashboard');
    setAnalysisContext(null);
  };

  if (currentView === 'analysis' && analysisContext) {
    return (
      <AnalysisView
        alert={analysisContext.alert}
        service={analysisContext.service}
        query={analysisContext.query}
        onBack={handleBackToDashboard}
      />
    );
  }

  return (
    <Dashboard
      alerts={mockAlerts}
      services={mockServices}
      incidentHistory={mockIncidentHistory}
      onAnalyzeAlert={handleAnalyzeAlert}
      onAnalyzeService={handleAnalyzeService}
      onServiceDetails={handleServiceDetails}
      onAlertDetails={handleAlertDetails}
    />
  );
}

export default App;
