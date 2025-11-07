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

// Analysis types
export interface RCAData {
  root_cause: string;
  evidence: string[];
  recommendations: string[];
}

export interface RunbookAction {
  action_title: string;
  steps: string[];
  source_document: string;
  source_url: string;
  relevance_score?: number;
}

export interface AnalysisUpdate {
  type: 'status' | 'rca_complete' | 'runbook_complete' | 'error';
  message?: string;
  rca?: RCAData;
  runbooks?: RunbookAction[];
}

