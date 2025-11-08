import React from 'react';
import type { IncidentHistoryEntry } from '../types';

interface IncidentHistorySectionProps {
  incidents: IncidentHistoryEntry[];
}

const severityClassMap: Record<IncidentHistoryEntry['severity'], string> = {
  P1: 'critical',
  P2: 'warning',
  P3: 'neutral',
  P4: 'neutral',
};

const severityLabelMap: Record<IncidentHistoryEntry['severity'], string> = {
  P1: '🔴 P1',
  P2: '🟡 P2',
  P3: '🟢 P3',
  P4: '🟢 P4',
};

const IncidentHistorySection: React.FC<IncidentHistorySectionProps> = ({ incidents }) => {
  if (!incidents.length) {
    return null;
  }

  return (
    <div className="incident-history-section">
      <div className="section-header">
        <span>🗂️ Incident History</span>
      </div>
      <div className="incident-history-grid">
        {incidents.map((incident) => {
          const severityClass = severityClassMap[incident.severity] ?? 'neutral';
          const severityLabel = severityLabelMap[incident.severity] ?? incident.severity;

          return (
            <div key={incident.id} className={`incident-card ${severityClass}`}>
              <div className="incident-card-header">
                <span className={`incident-severity ${severityClass}`}>{severityLabel}</span>
                <div className="incident-title">{incident.title}</div>
              </div>
              <div className="incident-meta">
                <span className="incident-meta-item">
                  <strong>Occurred:</strong> {incident.occurred}
                </span>
                {incident.scenario && (
                  <span className="incident-meta-item">
                    <strong>Scenario:</strong> {incident.scenario.replace(/_/g, ' ')}
                  </span>
                )}
              </div>
              <div className="incident-summary">
                {incident.summary}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default IncidentHistorySection;

