import type { Alert, Service, IncidentHistoryEntry } from '../types';

export const mockAlerts: Alert[] = [
  {
    id: 'alert-current-web',
    severity: 'P1',
    title: 'Web Tier 5xx Spike',
    started: 'Nov 8, 3:05 AM',
    affects: 'Edge/API traffic',
    description: 'Apache front end exceeding MaxRequestWorkers; intermittent 502/503.',
    scenario: 'scenario1_web_issue',
    status: 'active',
  },
];

export const mockIncidentHistory: IncidentHistoryEntry[] = [
  {
    id: 'incident-app-jul',
    occurred: 'Jul 14, 02:30 AM',
    severity: 'P2',
    title: 'App Tier JVM Exceptions',
    summary: 'NullPointerException and OOM across backend-sg services.',
    scenario: 'scenario2_app_issue',
  },
  {
    id: 'incident-db-mar',
    occurred: 'Mar 22, 11:10 PM',
    severity: 'P1',
    title: 'Database Deadlock Storm',
    summary: 'Lock waits and pool exhaustion on whizlabs-db.',
    scenario: 'scenario3_db_issue',
  },
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

