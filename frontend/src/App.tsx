import Dashboard from './components/Dashboard';
import { mockAlerts, mockServices } from './data/mockData';
import { analyzeIncident } from './services/api';
import './styles/globals.css';
import './styles/dashboard.css';

function App() {
  const handleAnalyzeAlert = async (alertId: string) => {
    const alert = mockAlerts.find(a => a.id === alertId);
    if (!alert) {
      console.error('Alert not found:', alertId);
      return;
    }

    try {
      const query = `${alert.title}. ${alert.description || ''} Affects: ${alert.affects}`;
      const response = await analyzeIncident({
        alert_id: alertId,
        query: query
      });
      console.log('Analysis response:', response);
      // TODO: Show results in UI (modal or results view)
      window.alert(`Analysis: ${response.message || response.response || 'Analysis started'}`);
    } catch (error) {
      console.error('Error analyzing alert:', error);
      window.alert(`Error: ${error instanceof Error ? error.message : 'Failed to analyze'}`);
    }
  };

  const handleAnalyzeService = async (serviceId: string) => {
    const service = mockServices.find(s => s.id === serviceId);
    if (!service) {
      console.error('Service not found:', serviceId);
      return;
    }

    try {
      const query = `Analyze service ${service.name} in ${service.environment}. Status: ${service.status}`;
      const response = await analyzeIncident({
        service_id: serviceId,
        query: query
      });
      console.log('Analysis response:', response);
      // TODO: Show results in UI (modal or results view)
      window.alert(`Analysis: ${response.message || response.response || 'Analysis started'}`);
    } catch (error) {
      console.error('Error analyzing service:', error);
      window.alert(`Error: ${error instanceof Error ? error.message : 'Failed to analyze'}`);
    }
  };

  const handleServiceDetails = (serviceId: string) => {
    console.log('Viewing service details:', serviceId);
    // TODO: Navigate to service details view
  };

  const handleAlertDetails = (alertId: string) => {
    console.log('Viewing alert details:', alertId);
    // TODO: Navigate to alert details view
  };

  return (
    <Dashboard
      alerts={mockAlerts}
      services={mockServices}
      onAnalyzeAlert={handleAnalyzeAlert}
      onAnalyzeService={handleAnalyzeService}
      onServiceDetails={handleServiceDetails}
      onAlertDetails={handleAlertDetails}
    />
  );
}

export default App;
