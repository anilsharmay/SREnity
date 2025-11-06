import React from 'react';
import type { Alert } from '../types';
import AlertCard from './AlertCard';

interface AlertsSectionProps {
  alerts: Alert[];
  onAnalyze: (alertId: string) => void;
  onViewDetails?: (alertId: string) => void;
}

const AlertsSection: React.FC<AlertsSectionProps> = ({ 
  alerts, 
  onAnalyze, 
  onViewDetails 
}) => {
  if (alerts.length === 0) {
    return null;
  }

  return (
    <div className="alerts-section">
      <div className="section-header">
        <span>🚨 Active Alerts ({alerts.length})</span>
      </div>
      <div className="alerts-grid">
        {alerts.map((alert) => (
          <AlertCard
            key={alert.id}
            alert={alert}
            onAnalyze={onAnalyze}
            onViewDetails={onViewDetails}
          />
        ))}
      </div>
    </div>
  );
};

export default AlertsSection;

