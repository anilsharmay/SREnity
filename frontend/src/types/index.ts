export interface Alert {
  id: string;
  severity: 'P1' | 'P2' | 'P3' | 'P4';
  title: string;
  started: string;
  affects: string;
  description?: string;
}

export interface Service {
  id: string;
  name: string;
  environment: string;
  type: string;
  latency: {
    value: number;
    unit: string;
    sparkline: number[];
  };
  throughput: {
    value: number;
    unit: string;
    sparkline: number[];
  };
  errorRate: {
    value: number;
    sparkline: number[];
  };
  status: 'healthy' | 'degraded' | 'critical';
}

