import React from 'react';
import type { Service } from '../types';
import ServiceRow from './ServiceRow';

interface ServicesTableProps {
  services: Service[];
  onServiceClick: (serviceId: string) => void;
  onAnalyze: (serviceId: string) => void;
  onViewDetails?: (serviceId: string) => void;
}

const ServicesTable: React.FC<ServicesTableProps> = ({ 
  services, 
  onServiceClick,
  onAnalyze,
  onViewDetails
}) => {
  return (
    <div className="services-table-container">
      <table className="services-table">
        <thead>
          <tr>
            <th>Service</th>
            <th>Environment</th>
            <th>Type</th>
            <th>Latency (avg)</th>
            <th>Throughput</th>
            <th>Error rate %</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {services.map((service) => (
            <ServiceRow
              key={service.id}
              service={service}
              onRowClick={onServiceClick}
              onAnalyze={onAnalyze}
              onViewDetails={onViewDetails}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ServicesTable;

