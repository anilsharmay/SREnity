import React from 'react';
import type { Alert } from '../types';
import ThreeDotMenu from './ThreeDotMenu';

interface AlertCardProps {
  alert: Alert;
  onAnalyze: (alertId: string) => void;
  onViewDetails?: (alertId: string) => void;
}

const AlertCard: React.FC<AlertCardProps> = ({ alert, onAnalyze, onViewDetails }) => {
  const handleMenuAction = (action: string) => {
    if (action === 'analyze') {
      onAnalyze(alert.id);
    } else if (action === 'details' && onViewDetails) {
      onViewDetails(alert.id);
    }
  };

  const menuOptions = [
    { label: 'View Details', action: 'details' },
    { label: 'Analyze with SREnity', action: 'analyze', isAnalyze: true }
  ];

  return (
    <div className={`alert-card ${alert.severity === 'P1' ? 'critical' : 'warning'}`}>
      <div className="alert-header">
        <div className={`alert-severity ${alert.severity === 'P1' ? 'critical' : 'warning'}`}>
          <span>{alert.severity === 'P1' ? '🔴' : '🟡'}</span>
          <span>{alert.severity}</span>
        </div>
        <div className="alert-title">{alert.title}</div>
        <ThreeDotMenu options={menuOptions} onSelect={handleMenuAction} />
      </div>
      <div className="alert-details">
        <div className="alert-detail-item">
          <span>Started:</span>
          <span>{alert.started}</span>
        </div>
        <div className="alert-detail-item">
          <span>Affects:</span>
          <span>{alert.affects}</span>
        </div>
        {alert.description && (
          <div className="alert-detail-item" style={{ width: '100%', marginTop: '8px' }}>
            <span>{alert.description}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default AlertCard;

