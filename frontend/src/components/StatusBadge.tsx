import React from 'react';

interface StatusBadgeProps {
  status: 'healthy' | 'degraded' | 'critical';
}

const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const getStatusIcon = () => {
    switch (status) {
      case 'critical':
        return '🔴';
      case 'degraded':
        return '🟡';
      case 'healthy':
        return '🟢';
      default:
        return '⚪';
    }
  };

  const getStatusLabel = () => {
    switch (status) {
      case 'critical':
        return 'Critical';
      case 'degraded':
        return 'Degraded';
      case 'healthy':
        return 'Healthy';
      default:
        return 'Unknown';
    }
  };

  return (
    <span className={`status-badge ${status}`}>
      <span>{getStatusIcon()}</span>
      <span>{getStatusLabel()}</span>
    </span>
  );
};

export default StatusBadge;

