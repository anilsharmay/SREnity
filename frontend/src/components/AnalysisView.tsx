import React, { useState, useEffect, useMemo } from 'react';
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

  const summarySections = useMemo(() => {
    if (!rca?.summary_sections || rca.summary_sections.length === 0) {
      return [];
    }

    type Section = {
      title: string;
      paragraphs: string[];
      bullets: string[];
      numbered: string[];
    };

    const sections: Section[] = [];
    const formatInline = (text: string) =>
      text.replace(/\*\*(.+?)\*\*/g, '$1').replace(/`([^`]+)`/g, '$1');

    for (const section of rca.summary_sections) {
      const parsed: Section = {
        title: formatInline(section.title),
        paragraphs: [],
        bullets: [],
        numbered: [],
      };

      const lines = section.content.split('\n');
      for (const rawLine of lines) {
        const line = rawLine.trim();
        if (!line || line === '---') {
          continue;
        }

        if (line.startsWith('- ')) {
          parsed.bullets.push(formatInline(line.slice(2).trim()));
        } else if (/^\d+\./.test(line)) {
          const stepText = line.replace(/^\d+\.\s*/, '');
          parsed.numbered.push(formatInline(stepText));
        } else {
          parsed.paragraphs.push(formatInline(line));
        }
      }

      sections.push(parsed);
    }

    return sections;
  }, [rca?.summary_sections]);

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
            {summarySections.length > 0 ? (
              <div className="rca-section">
                <h3>Root Cause Analysis Summary</h3>
                <div className="rca-summary-grid">
                  {summarySections.map((section, idx) => (
                    <div key={idx} className="rca-summary-card">
                      <h4>{section.title}</h4>
                      {section.paragraphs.map((paragraph, pIdx) => (
                        <p key={pIdx}>{paragraph}</p>
                      ))}
                      {section.bullets.length > 0 && (
                        <ul>
                          {section.bullets.map((item, bIdx) => (
                            <li key={bIdx}>{item}</li>
                          ))}
                        </ul>
                      )}
                      {section.numbered.length > 0 && (
                        <ol>
                          {section.numbered.map((item, nIdx) => (
                            <li key={nIdx}>{item}</li>
                          ))}
                        </ol>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="rca-section">
                <h3>Root Cause Analysis Summary</h3>
                <div className="summary-text">
                  <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                    {rca.summary || rca.root_cause}
                  </pre>
                </div>
              </div>
            )}

            {/* Tier-specific Results */}
            {(rca.web_result || rca.app_result || rca.db_result) && (
              <div className="rca-section">
                <h3>Layer Analysis Results</h3>
                {rca.web_result && (
                  <div className="tier-result">
                    <h4>Web Tier Analysis</h4>
                    <p className="tier-text">{rca.web_result}</p>
                  </div>
                )}
                {rca.app_result && (
                  <div className="tier-result">
                    <h4>App Tier Analysis</h4>
                    <p className="tier-text">{rca.app_result}</p>
                  </div>
                )}
                {rca.db_result && (
                  <div className="tier-result">
                    <h4>DB Tier Analysis</h4>
                    <p className="tier-text">{rca.db_result}</p>
                  </div>
                )}
                {rca.cache_result && (
                  <div className="tier-result">
                    <h4>Cache Tier Analysis</h4>
                    <p className="tier-text">{rca.cache_result}</p>
                  </div>
                )}
              </div>
            )}

            {rca.evidence && rca.evidence.length > 0 && (
              <div className="rca-section">
                <h3>Evidence Summary</h3>
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
          <h2 className="section-title">Recommended Runbooks</h2>
          <div className="runbooks-list">
            {runbooks.map((runbook, index) => (
              <div key={index} className="runbook-item">
                <div className="runbook-title">{runbook.action_title}</div>
                {runbook.source_url ? (
                  <a
                    href={runbook.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="runbook-link"
                  >
                    View →
                  </a>
                ) : (
                  <span className="no-link">N/A</span>
                )}
              </div>
            ))}
          </div>
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

