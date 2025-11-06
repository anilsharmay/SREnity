import React from 'react';
import type { Service } from '../types';
import StatusBadge from './StatusBadge';
import Sparkline from './Sparkline';
import ThreeDotMenu from './ThreeDotMenu';

interface ServiceRowProps {
  service: Service;
  onRowClick: (serviceId: string) => void;
  onAnalyze: (serviceId: string) => void;
  onViewDetails?: (serviceId: string) => void;
}

const ServiceRow: React.FC<ServiceRowProps> = ({ 
  service, 
  onRowClick, 
  onAnalyze,
  onViewDetails 
}) => {
  const handleMenuAction = (action: string) => {
    if (action === 'analyze') {
      onAnalyze(service.id);
    } else if (action === 'details' && onViewDetails) {
      onViewDetails(service.id);
    } else if (action === 'details') {
      onRowClick(service.id);
    }
  };

  const menuOptions = [
    { label: 'View Service Details', action: 'details' },
    { label: 'Analyze with SREnity', action: 'analyze', isAnalyze: true }
  ];

  const getErrorRateColor = () => {
    if (service.errorRate.value > 5) return '#dc3545';
    if (service.errorRate.value > 1) return '#ffc107';
    return '#6c757d';
  };

  return (
    <tr 
      className="service-row"
      onClick={() => onRowClick(service.id)}
    >
      <td>
        <div className="service-name-cell">
          <div className="service-name">{service.name}</div>
          <StatusBadge status={service.status} />
        </div>
      </td>
      <td>
        <div className="service-meta">
          {service.environment}
        </div>
      </td>
      <td>
        <div className="service-meta">
          {service.type}
        </div>
      </td>
      <td>
        <div className="metric-cell">
          <span className="metric-value">
            {service.latency.value} {service.latency.unit}
          </span>
          <Sparkline data={service.latency.sparkline} />
        </div>
      </td>
      <td>
        <div className="metric-cell">
          <span className="metric-value">
            {service.throughput.value.toFixed(1)} {service.throughput.unit}
          </span>
          <Sparkline data={service.throughput.sparkline} />
        </div>
      </td>
      <td>
        <div className="metric-cell">
          <span className="metric-value" style={{ 
            color: service.errorRate.value > 0 ? getErrorRateColor() : undefined 
          }}>
            {service.errorRate.value.toFixed(1)}%
            {service.errorRate.value > 0 && ' ⚠️'}
          </span>
          <Sparkline 
            data={service.errorRate.sparkline} 
            color={getErrorRateColor()}
          />
        </div>
      </td>
      <td className="actions-cell">
        <div onClick={(e) => e.stopPropagation()}>
          <ThreeDotMenu options={menuOptions} onSelect={handleMenuAction} />
        </div>
      </td>
    </tr>
  );
};

export default ServiceRow;

