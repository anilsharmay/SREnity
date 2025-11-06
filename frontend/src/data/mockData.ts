import type { Alert, Service } from '../types';

export const mockAlerts: Alert[] = [
  {
    id: 'alert-001',
    severity: 'P1',
    title: 'Database Cluster Connection Issues',
    started: '3:15 AM',
    affects: 'Multiple services',
    description: 'Connection pool exhausted across database cluster'
  },
  {
    id: 'alert-002',
    severity: 'P2',
    title: 'API Gateway Rate Limiting',
    started: '2:45 AM',
    affects: 'All API services',
    description: 'Rate limit threshold reached, throttling requests'
  }
];

// Generate mock sparkline data (simple trend)
const generateSparkline = (count: number, base: number, variation: number): number[] => {
  return Array.from({ length: count }, () => 
    base + Math.random() * variation - variation / 2
  );
};

export const mockServices: Service[] = [
  {
    id: 'service-001',
    name: 'opbeans-java',
    environment: 'production',
    type: 'service',
    latency: {
      value: 156,
      unit: 'ms',
      sparkline: generateSparkline(20, 150, 30)
    },
    throughput: {
      value: 89.1,
      unit: 'tpm',
      sparkline: generateSparkline(20, 85, 15)
    },
    errorRate: {
      value: 6.0,
      sparkline: generateSparkline(20, 5, 2)
    },
    status: 'critical'
  },
  {
    id: 'service-002',
    name: 'opbeans-dotnet',
    environment: 'production',
    type: 'service',
    latency: {
      value: 89,
      unit: 'ms',
      sparkline: generateSparkline(20, 85, 20)
    },
    throughput: {
      value: 45.2,
      unit: 'tpm',
      sparkline: generateSparkline(20, 45, 10)
    },
    errorRate: {
      value: 2.6,
      sparkline: generateSparkline(20, 2, 1)
    },
    status: 'degraded'
  },
  {
    id: 'service-003',
    name: 'apm-server',
    environment: 'production',
    type: 'service',
    latency: {
      value: 51,
      unit: 'ms',
      sparkline: generateSparkline(20, 50, 10)
    },
    throughput: {
      value: 751.4,
      unit: 'tpm',
      sparkline: generateSparkline(20, 750, 50)
    },
    errorRate: {
      value: 0.0,
      sparkline: generateSparkline(20, 0, 0.5)
    },
    status: 'healthy'
  },
  {
    id: 'service-004',
    name: 'kibana',
    environment: 'production',
    type: 'service',
    latency: {
      value: 234,
      unit: 'ms',
      sparkline: generateSparkline(20, 230, 30)
    },
    throughput: {
      value: 12.3,
      unit: 'tpm',
      sparkline: generateSparkline(20, 12, 3)
    },
    errorRate: {
      value: 0.0,
      sparkline: generateSparkline(20, 0, 0.5)
    },
    status: 'healthy'
  },
  {
    id: 'service-005',
    name: 'opbeans-ruby',
    environment: 'production',
    type: 'service',
    latency: {
      value: 67,
      unit: 'ms',
      sparkline: generateSparkline(20, 65, 15)
    },
    throughput: {
      value: 234.5,
      unit: 'tpm',
      sparkline: generateSparkline(20, 230, 30)
    },
    errorRate: {
      value: 0.0,
      sparkline: generateSparkline(20, 0, 0.5)
    },
    status: 'healthy'
  },
  {
    id: 'service-006',
    name: 'opbeans-python',
    environment: 'production',
    type: 'service',
    latency: {
      value: 123,
      unit: 'ms',
      sparkline: generateSparkline(20, 120, 20)
    },
    throughput: {
      value: 156.7,
      unit: 'tpm',
      sparkline: generateSparkline(20, 155, 25)
    },
    errorRate: {
      value: 0.0,
      sparkline: generateSparkline(20, 0, 0.5)
    },
    status: 'healthy'
  },
  {
    id: 'service-007',
    name: 'kibana-frontend',
    environment: 'production',
    type: 'frontend',
    latency: {
      value: 45,
      unit: 'ms',
      sparkline: generateSparkline(20, 44, 8)
    },
    throughput: {
      value: 567.8,
      unit: 'tpm',
      sparkline: generateSparkline(20, 565, 40)
    },
    errorRate: {
      value: 0.0,
      sparkline: generateSparkline(20, 0, 0.5)
    },
    status: 'healthy'
  }
];

