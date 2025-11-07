import React, { useState, useEffect } from 'react';
import { useAnalysisStream } from '../hooks/useAnalysisStream';
import type { Alert, Service } from '../types';
import '../styles/analysis.css';

interface AnalysisViewProps {
  alert?: Alert;
  service?: Service;
  query: string;
  onBack: () => void;
}

const AnalysisView: React.FC<AnalysisViewProps> = ({ alert, service, query, onBack }) => {
  const [expandedRunbook, setExpandedRunbook] = useState<number | null>(null);
  const [showStatusLog, setShowStatusLog] = useState(false);

  const {
    statusMessages,
    rca,
    runbooks,
    isStreaming,
    error,
    startAnalysis,
    stopAnalysis,
  } = useAnalysisStream({
    alertId: alert?.id,
    serviceId: service?.id,
    query: query,
    onComplete: () => {
      console.log('Analysis complete');
    },
    onError: (err) => {
      console.error('Analysis error:', err);
    },
  });

  useEffect(() => {
    // Start analysis when component mounts
    startAnalysis();

    // Cleanup on unmount
    return () => {
      stopAnalysis();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Only run once on mount

  // Determine progress steps
  const steps = [
    { id: 'retrieve', label: 'Retrieving Logs & Metrics', complete: statusMessages.length > 0 },
    { id: 'analyze', label: 'Analyzing Patterns', complete: statusMessages.some(msg => msg.includes('Analyzing') || msg.includes('Pattern')) },
    { id: 'rca', label: 'RCA Summary', complete: !!rca },
    { id: 'runbooks', label: 'Runbook Search', complete: runbooks.length > 0 },
  ];

  const currentStep = steps.findIndex(step => !step.complete);
  const activeStepIndex = currentStep === -1 ? steps.length - 1 : currentStep;

  return (
    <div className="analysis-container">
      {/* Header */}
      <div className="analysis-header">
        <button className="back-button" onClick={onBack}>
          ← Back
        </button>
        <h1>SREnity Analysis</h1>
      </div>

      {/* Progress Timeline */}
      <div className="progress-timeline">
        {steps.map((step, index) => (
          <div
            key={step.id}
            className={`progress-step ${step.complete ? 'complete' : ''} ${index === activeStepIndex && !step.complete && isStreaming ? 'active' : ''}`}
          >
            <div className="step-indicator">
              {step.complete ? '✓' : index === activeStepIndex && isStreaming ? '→' : '○'}
            </div>
            <div className="step-label">{step.label}</div>
          </div>
        ))}
      </div>

      {/* Error Display */}
      {error && (
        <div className="error-card">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      )}

      {/* RCA Section */}
      {rca && (
        <div className="rca-card">
          <div className="card-header">
            <h2>Root Cause Analysis</h2>
            <span className="status-badge complete">Complete</span>
          </div>
          <div className="card-content">
            <div className="rca-section">
              <h3>Root Cause Identified</h3>
              <p className="root-cause-text">{rca.root_cause}</p>
            </div>

            {rca.evidence && rca.evidence.length > 0 && (
              <div className="rca-section">
                <h3>Evidence</h3>
                <ul className="evidence-list">
                  {rca.evidence.map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>
            )}

            {rca.recommendations && rca.recommendations.length > 0 && (
              <div className="rca-section">
                <h3>Resolution Recommendations</h3>
                <ul className="recommendations-list">
                  {rca.recommendations.map((rec, idx) => (
                    <li key={idx}>{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Runbook Actions */}
      {runbooks.length > 0 && (
        <div className="runbooks-section">
          <h2 className="section-title">Recommended Actions (from Runbooks)</h2>
          {runbooks.map((runbook, index) => (
            <div key={index} className="runbook-card">
              <div className="runbook-header">
                <h3>{runbook.action_title}</h3>
                {runbook.relevance_score !== undefined && (
                  <span className="relevance-badge">
                    {(runbook.relevance_score * 100).toFixed(0)}% relevant
                  </span>
                )}
              </div>
              <div className="runbook-content">
                {runbook.steps && runbook.steps.length > 0 && (
                  <div className="runbook-steps">
                    <button
                      className="steps-toggle"
                      onClick={() => setExpandedRunbook(expandedRunbook === index ? null : index)}
                    >
                      {expandedRunbook === index ? '▼' : '▶'} Steps ({runbook.steps.length})
                    </button>
                    {expandedRunbook === index && (
                      <ol className="steps-list">
                        {runbook.steps.map((step, stepIdx) => (
                          <li key={stepIdx}>{step}</li>
                        ))}
                      </ol>
                    )}
                  </div>
                )}
                <div className="runbook-source">
                  <span className="source-label">📄 Source:</span>
                  <span className="source-document">{runbook.source_document}</span>
                  {runbook.source_url && (
                    <a
                      href={runbook.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="source-link"
                    >
                      View full runbook →
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Status Log */}
      <div className="status-log-section">
        <button
          className="status-log-toggle"
          onClick={() => setShowStatusLog(!showStatusLog)}
        >
          {showStatusLog ? '▼' : '▶'} Status Log ({statusMessages.length})
        </button>
        {showStatusLog && (
          <div className="status-log">
            {statusMessages.map((message, index) => (
              <div key={index} className="status-log-entry">
                <span className="status-time">{new Date().toLocaleTimeString()}</span>
                <span className="status-message">{message}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalysisView;

