/**
 * API service for SREnity backend
 */
const API_URL = 'http://localhost:8000';

export interface AnalyzeRequest {
  alert_id?: string;
  service_id?: string;
  query: string;
}

export interface AnalyzeResponse {
  status: string;
  message?: string;
  response?: string;
}

export async function analyzeIncident(request: AnalyzeRequest): Promise<AnalyzeResponse> {
  const response = await fetch(`${API_URL}/api/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }
  
  return response.json();
}

