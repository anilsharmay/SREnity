import Dashboard from './components/Dashboard';
import { mockAlerts, mockServices } from './data/mockData';
import './styles/globals.css';
import './styles/dashboard.css';

function App() {
  const handleAnalyzeAlert = (alertId: string) => {
    // TODO: Connect to FastAPI backend
    console.log('Analyzing alert:', alertId);
    alert(`Analyzing alert ${alertId} with SREnity... (This will connect to backend)`);
  };

  const handleAnalyzeService = (serviceId: string) => {
    // TODO: Connect to FastAPI backend
    console.log('Analyzing service:', serviceId);
    alert(`Analyzing service ${serviceId} with SREnity... (This will connect to backend)`);
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
