import React, { useState, useEffect, useMemo } from 'react';
import { useAnalysisStream } from '../hooks/useAnalysisStream';
import type { Alert, Service } from '../types';
import '../styles/analysis.css';
import {
  HiDocumentText,
  HiCollection,
  HiSearch,
  HiBookOpen,
} from 'react-icons/hi';
import type { IconType } from 'react-icons';

type StructuredSection = {
  title: string;
  paragraphs: string[];
  bullets: string[];
  numbered: string[];
};

const stripInlineFormatting = (text: string) =>
  text.replace(/\*\*(.+?)\*\*/g, '$1').replace(/`([^`]+)`/g, '$1').trim();

const parseStructuredSections = (
  sections?: Array<{
    title: string;
    content: string;
  }>,
): StructuredSection[] => {
  if (!sections || sections.length === 0) {
    return [];
  }

  const parsedSections: StructuredSection[] = [];

  for (const section of sections) {
    const parsed: StructuredSection = {
      title: stripInlineFormatting(section.title),
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
        parsed.bullets.push(stripInlineFormatting(line.slice(2).trim()));
      } else if (/^\d+\./.test(line)) {
        const stepText = line.replace(/^\d+\.\s*/, '');
        parsed.numbered.push(stripInlineFormatting(stepText));
      } else {
        parsed.paragraphs.push(stripInlineFormatting(line));
      }
    }

    parsedSections.push(parsed);
  }

  return parsedSections;
};

const parseMarkdownSummary = (markdown?: string | null): StructuredSection[] => {
  if (!markdown) {
    return [];
  }

  const lines = markdown.split('\n');
  const sections: Array<{ title: string; content: string }> = [];
  let currentTitle: string | null = null;
  let currentContent: string[] = [];

  const pushSection = () => {
    if (!currentTitle) {
      return;
    }
    sections.push({
      title: currentTitle,
      content: currentContent.join('\n').trim(),
    });
    currentTitle = null;
    currentContent = [];
  };

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line) {
      currentContent.push('');
      continue;
    }

    const headingMatch = line.match(/^#{1,6}\s*(.+)$/);
    if (headingMatch) {
      pushSection();
      currentTitle = stripInlineFormatting(headingMatch[1]);
      currentContent = [];
      continue;
    }

    currentContent.push(line);
  }

  if (currentTitle) {
    pushSection();
  }

  return parseStructuredSections(sections);
};

const hasSectionContent = (section?: StructuredSection | null) =>
  !!section &&
  (section.paragraphs.length > 0 ||
    section.bullets.length > 0 ||
    section.numbered.length > 0);

const normalizeTitle = (title: string) => title.replace(/[:]/g, '').trim().toLowerCase();

const getDisplayTitle = (title: string): string => {
  const titleMap: Record<string, string> = {
    'Root Cause Analysis': 'Root Cause',
    'Impact Assessment': 'Impact',
  };
  return titleMap[title] || title;
};

// Icon mapping for section headers
const getHeaderIcon = (title: string): { Icon: IconType; color: string; size: number } | null => {
  const normalized = title.toLowerCase().trim();
  
  if (normalized === 'executive summary') {
    return { Icon: HiDocumentText, color: '#b8c5d6', size: 20 };
  }
  if (normalized === 'incident deep dive') {
    return { Icon: HiCollection, color: '#8b5cf6', size: 20 };
  }
  if (normalized === 'root cause analysis') {
    return { Icon: HiSearch, color: '#3b82f6', size: 20 };
  }
  if (normalized === 'recommended runbooks') {
    return { Icon: HiBookOpen, color: '#10b981', size: 20 };
  }
  
  return null;
};

// Helper component to render header icon
const HeaderIcon: React.FC<{ title: string }> = ({ title }) => {
  const iconConfig = getHeaderIcon(title);
  if (!iconConfig) return null;
  
  const { Icon, color, size } = iconConfig;
  return <Icon color={color} size={size} style={{ flexShrink: 0 }} />;
};

interface AnalysisViewProps {
  alert?: Alert;
  service?: Service;
  query: string;
  onBack: () => void;
}

const AnalysisView: React.FC<AnalysisViewProps> = ({ alert, service, query, onBack }) => {
  const [showStatusLog, setShowStatusLog] = useState(false);
  const [isDeepDiveExpanded, setDeepDiveExpanded] = useState(false);

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
    // eslint-disable-next-line react-hooks-exhaustive-deps
  }, []); // Only run once on mount

  const structuredSummarySections = useMemo(() => {
    if (rca?.summary_sections?.length) {
      return parseStructuredSections(rca.summary_sections);
    }
    return [];
  }, [rca?.summary_sections]);

  const finalSummarySections = useMemo(
    () => parseMarkdownSummary(rca?.full_summary ?? rca?.summary),
    [rca?.full_summary, rca?.summary],
  );

  const summarySections = useMemo(() => {
    if (structuredSummarySections.length > 0) {
      return structuredSummarySections;
    }
    if (finalSummarySections.length > 0) {
      return finalSummarySections;
    }
    return parseMarkdownSummary(rca?.root_cause);
  }, [structuredSummarySections, finalSummarySections, rca?.root_cause]);

  const rcaSummaryCards = useMemo(() => {
    const allowed = new Set([
      normalizeTitle('Root Cause Analysis'),
      normalizeTitle('Impact Assessment'),
    ]);
    return summarySections.filter((section) => allowed.has(normalizeTitle(section.title)));
  }, [summarySections]);

  const executiveSummarySection = useMemo(() => {
    const execSection = finalSummarySections.find(
      (section) => normalizeTitle(section.title) === normalizeTitle('Executive Summary'),
    );
    if (execSection && hasSectionContent(execSection)) {
      return execSection;
    }
    if (rca?.summary) {
      return {
        title: 'Executive Summary',
        paragraphs: [stripInlineFormatting(rca.summary)],
        bullets: [],
        numbered: [],
      };
    }
    return null;
  }, [finalSummarySections, rca?.summary]);

  const deepDiveSections = useMemo(() => {
    if (!rca) {
      return [];
    }

    const parsedMap = new Map<string, StructuredSection>();

    finalSummarySections.forEach((section) => {
      parsedMap.set(normalizeTitle(section.title), section);
    });

    summarySections.forEach((section) => {
      if (!parsedMap.has(normalizeTitle(section.title))) {
        parsedMap.set(normalizeTitle(section.title), section);
      }
    });

    const ensureSection = (
      title: string,
      fallback?: () => StructuredSection | null,
    ): StructuredSection | null => {
      const existing = parsedMap.get(normalizeTitle(title));
      if (hasSectionContent(existing)) {
        return {
          title,
          paragraphs: existing!.paragraphs,
          bullets: existing!.bullets,
          numbered: existing!.numbered,
        };
      }

      if (fallback) {
        const built = fallback();
        if (hasSectionContent(built)) {
          return built!;
        }
      }

      return null;
    };

    const tierBullets: string[] = [];
    if (rca.tier_analysis && rca.tier_analysis.length > 0) {
      rca.tier_analysis.forEach((tier) => {
        const title = stripInlineFormatting(tier.title ?? '');
        const parts: string[] = [];
        if (tier.status) {
          parts.push(`Status: ${stripInlineFormatting(tier.status)}`);
        }
        if (tier.severity) {
          parts.push(`Severity: ${stripInlineFormatting(tier.severity)}`);
        }
        if (tier.summary) {
          parts.push(stripInlineFormatting(tier.summary));
        }
        if (tier.details && tier.details.length > 0) {
          parts.push(stripInlineFormatting(tier.details.join(' ')));
        }
        const bulletText =
          (title ? `${title}: ` : '') + (parts.length > 0 ? parts.join(' | ') : '');
        if (bulletText.trim()) {
          tierBullets.push(bulletText.trim());
        }
      });
    } else {
      if (rca.web_result) {
        tierBullets.push(`Web Tier: ${stripInlineFormatting(rca.web_result)}`);
      }
      if (rca.app_result) {
        tierBullets.push(`App Tier: ${stripInlineFormatting(rca.app_result)}`);
      }
      if (rca.db_result) {
        tierBullets.push(`DB Tier: ${stripInlineFormatting(rca.db_result)}`);
      }
      if (rca.cache_result) {
        tierBullets.push(`Cache Tier: ${stripInlineFormatting(rca.cache_result)}`);
      }
    }

    const sections: Array<StructuredSection | null> = [
      ensureSection('Tier Analysis', () => {
        if (tierBullets.length === 0) {
          return null;
        }
        return {
          title: 'Tier Analysis',
          paragraphs: [],
          bullets: tierBullets,
          numbered: [],
        };
      }),
      ensureSection('Cross-Tier Correlations', () => {
        if (rca.evidence && rca.evidence.length > 0) {
          return {
            title: 'Cross-Tier Correlations',
            paragraphs: [],
            bullets: rca.evidence.map(stripInlineFormatting),
            numbered: [],
          };
        }
        return {
          title: 'Cross-Tier Correlations',
          paragraphs: ['No cross-tier correlation anomalies were identified during this incident.'],
          bullets: [],
          numbered: [],
        };
      }),
      ensureSection('Root Cause Analysis', () => {
        if (!rca.root_cause) {
          return null;
        }
        return {
          title: 'Root Cause Analysis',
          paragraphs: [stripInlineFormatting(rca.root_cause)],
          bullets: [],
          numbered: [],
        };
      }),
      ensureSection('Impact Assessment', () => {
        const impactParagraphs: string[] = [];
        if (rca.summary) {
          impactParagraphs.push(stripInlineFormatting(rca.summary));
        }
        const impactBullets = (rca.evidence || []).map(stripInlineFormatting);

        if (impactParagraphs.length === 0 && impactBullets.length === 0) {
          return null;
        }

        return {
          title: 'Impact Assessment',
          paragraphs: impactParagraphs,
          bullets: impactBullets,
          numbered: [],
        };
      }),
      ensureSection('Remediation Plan', () => {
        if (!rca.recommendations || rca.recommendations.length === 0) {
          return null;
        }
        return {
          title: 'Remediation Plan',
          paragraphs: [],
          bullets: rca.recommendations.map(stripInlineFormatting),
          numbered: [],
        };
      }),
    ];

    return sections.filter((section): section is StructuredSection => hasSectionContent(section));
  }, [rca, summarySections, finalSummarySections]);

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
            className={`progress-step ${step.complete ? 'complete' : ''} ${
              index === activeStepIndex && !step.complete && isStreaming ? 'active' : ''
            }`}
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
        <>
          {executiveSummarySection && (
            <div className="rca-card">
              <div className="card-header">
                <h2>
                  <HeaderIcon title="Executive Summary" />
                  Executive Summary
                </h2>
              </div>
              <div className="card-content">
                {executiveSummarySection.paragraphs.map((paragraph, idx) => (
                  <p key={idx}>{paragraph}</p>
                ))}
                {executiveSummarySection.bullets.length > 0 && (
                  <ul>
                    {executiveSummarySection.bullets.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                )}
                {executiveSummarySection.numbered.length > 0 && (
                  <ol>
                    {executiveSummarySection.numbered.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ol>
                )}
              </div>
            </div>
          )}

          {deepDiveSections.length > 0 && (
            <div className="deep-dive-card">
              <div className="card-header">
                <div>
                  <h2>
                    <HeaderIcon title="Incident Deep Dive" />
                    Incident Deep Dive
                  </h2>
                  <p className="card-subtitle">Detailed breakdown of the incident response timeline</p>
                </div>
              </div>
              <div className="accordion-toggle">
                <button
                  type="button"
                  className="accordion-trigger"
                  onClick={() => setDeepDiveExpanded((prev) => !prev)}
                >
                  <span className="accordion-title">
                    {isDeepDiveExpanded ? 'Collapse Sections' : 'Expand Sections'}
                  </span>
                  <span className="accordion-icon">{isDeepDiveExpanded ? '−' : '+'}</span>
                </button>
              </div>
              {isDeepDiveExpanded && (
                <div className="accordion">
                  {deepDiveSections.map((section, index) => (
                    <div key={`${section.title}-${index}`} className="accordion-item expanded">
                      <div className="accordion-trigger static">
                        <span className="accordion-title">{section.title}</span>
                      </div>
                      <div className="accordion-content">
                        {section.paragraphs.map((paragraph, pIdx) => (
                          <p key={`paragraph-${pIdx}`}>{paragraph}</p>
                        ))}
                        {section.bullets.length > 0 && (
                          <ul>
                            {section.bullets.map((item, bIdx) => (
                              <li key={`bullet-${bIdx}`}>{item}</li>
                            ))}
                          </ul>
                        )}
                        {section.numbered.length > 0 && (
                          <ol>
                            {section.numbered.map((item, nIdx) => (
                              <li key={`numbered-${nIdx}`}>{item}</li>
                            ))}
                          </ol>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          <div className="rca-card">
            <div className="card-header">
              <h2>
                <HeaderIcon title="Root Cause Analysis" />
                Root Cause Analysis
              </h2>
              <span className="status-badge complete">Complete</span>
            </div>
            <div className="card-content">
              {rcaSummaryCards.length > 0 ? (
                <div className="rca-section">
                  <div className="rca-summary-grid">
                    {rcaSummaryCards.map((section, idx) => {
                      const items = [
                        ...section.paragraphs,
                        ...section.bullets,
                        ...section.numbered,
                      ].map(stripInlineFormatting);
                      return (
                        <div key={idx} className="rca-summary-card">
                          <h4>{getDisplayTitle(section.title)}</h4>
                          <ul className="rca-summary-inline-list">
                            {items.map((item, itemIdx) => (
                              <li key={itemIdx}>{item}</li>
                            ))}
                          </ul>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ) : (
                <div className="rca-section">
                  <div className="summary-text">
                    <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                      {rca.summary || rca.root_cause}
                    </pre>
                  </div>
                </div>
              )}

              {/* Tier-specific Results */}
              {(rca.web_result || rca.app_result || rca.db_result || rca.cache_result) && (
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
        </>
      )}

      {/* Runbook Actions */}
      {runbooks.length > 0 && (
        <div className="runbooks-section">
          <h2 className="section-title">
            <HeaderIcon title="Recommended Runbooks" />
            Recommended Runbooks
          </h2>
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

