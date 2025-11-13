/**
 * Hook for streaming analysis updates via Server-Sent Events
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import type { AnalysisUpdate, RCAData, RunbookAction } from '../types';

interface UseAnalysisStreamOptions {
  alertId?: string;
  serviceId?: string;
  query: string;
  onComplete?: () => void;
  onError?: (error: Error) => void;
}

interface AnalysisState {
  statusMessages: Array<{ message: string; timestamp: string }>;
  rca: RCAData | null;
  runbooks: RunbookAction[];
  isStreaming: boolean;
  error: string | null;
}

export function useAnalysisStream({
  alertId,
  serviceId,
  query,
  onComplete,
  onError,
}: UseAnalysisStreamOptions) {
  const [state, setState] = useState<AnalysisState>({
    statusMessages: [],
    rca: null,
    runbooks: [],
    isStreaming: false,
    error: null,
  });

  const abortControllerRef = useRef<AbortController | null>(null);

  const startAnalysis = useCallback(() => {
    // Abort existing request if any
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    setState({
      statusMessages: [],
      rca: null,
      runbooks: [],
      isStreaming: true,
      error: null,
    });

    // Build request body
    const requestBody = {
      alert_id: alertId,
      service_id: serviceId,
      query: query,
    };

    // Use fetch with POST for SSE (EventSource only supports GET)
    // We'll use a different approach: fetch with ReadableStream
    const controller = new AbortController();
    const signal = controller.signal;

    fetch('http://localhost:8000/api/analyze/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
      signal,
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) {
          throw new Error('No response body');
        }

        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();

          if (done) {
            setState((prev) => ({ ...prev, isStreaming: false }));
            onComplete?.();
            break;
          }

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6).trim();
              if (!data) {
                continue;
              }

              if (data === '[DONE]') {
                setState((prev) => ({ ...prev, isStreaming: false }));
                onComplete?.();
                return;
              }

              let parsed: AnalysisUpdate | null = null;
              try {
                parsed = JSON.parse(data) as AnalysisUpdate;
              } catch (e) {
                console.warn('Non-JSON SSE payload:', data, e);
              }

              if (!parsed) {
                setState((prev) => ({
                  ...prev,
                  statusMessages: [...prev.statusMessages, { 
                    message: data, 
                    timestamp: new Date().toLocaleTimeString() 
                  }],
                }));
                continue;
              }

              const update = parsed;

              if (update.type === 'status' && update.message) {
                setState((prev) => ({
                  ...prev,
                  statusMessages: [...prev.statusMessages, { 
                    message: update.message!, 
                    timestamp: new Date().toLocaleTimeString() 
                  }],
                }));
              } else if (update.type === 'rca_complete' && update.rca) {
                setState((prev) => ({
                  ...prev,
                  rca: update.rca ?? null,
                }));
              } else if (update.type === 'runbook_complete' && update.runbooks) {
                setState((prev) => ({
                  ...prev,
                  runbooks: update.runbooks ?? [],
                }));
              } else if (update.type === 'error') {
                const error = new Error(update.message || 'Unknown error');
                setState((prev) => ({
                  ...prev,
                  error: update.message || 'Unknown error',
                  isStreaming: false,
                }));
                onError?.(error);
              }
            }
          }
        }
      })
      .catch((error) => {
        if (error.name !== 'AbortError') {
          setState((prev) => ({
            ...prev,
            error: error.message,
            isStreaming: false,
          }));
          onError?.(error);
        }
      });

    // Store controller for cleanup
    abortControllerRef.current = controller;
  }, [alertId, serviceId, query, onComplete, onError]);

  const stopAnalysis = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setState((prev) => ({ ...prev, isStreaming: false }));
  }, []);

  useEffect(() => {
    return () => {
      stopAnalysis();
    };
  }, [stopAnalysis]);

  return {
    ...state,
    startAnalysis,
    stopAnalysis,
  };
}

