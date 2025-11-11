export interface Alert {
  id: string;
  severity: 'P1' | 'P2' | 'P3' | 'P4';
  title: string;
  started: string;
  affects: string;
  description?: string;
  scenario?: string;
  status?: 'active' | 'resolved';
}

export interface IncidentHistoryEntry {
  id: string;
  occurred: string;
  severity: Alert['severity'];
  title: string;
  summary: string;
  scenario?: string;
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
  summary?: string;  // Full summary
  full_summary?: string;
  evidence: string[];
  recommendations: string[];
  web_result?: string;  // Complete web tier analysis
  app_result?: string;  // Complete app tier analysis
  db_result?: string;  // Complete db tier analysis
  cache_result?: string;  // Complete cache tier analysis
  tier_analysis?: Array<{
    title: string;
    status?: string;
    severity?: string;
    summary?: string;
    details?: string[];
  }>;
  summary_sections?: Array<{
    title: string;
    content: string;
  }>;
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

