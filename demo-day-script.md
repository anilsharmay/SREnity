# SREnity Demo Day - Script & Goals

## 🎯 Demo Day Goal

Demonstrate an **end-to-end SRE incident resolution workflow** that combines:
1. **Root Cause Analysis (RCA)** - Automated log and metrics analysis to identify incident causes
2. **Runbook RAG** - Intelligent retrieval of relevant troubleshooting procedures from runbook knowledge base

The demo showcases how SREnity accelerates incident resolution by automating both diagnosis and solution retrieval, reducing MTTR and enabling faster incident response.

---

## 👤 User Journey

### Scenario: P1 Production Alert at 3 AM

**1. User lands on APM dashboard**
- User receives a P1 alert notification at 3 AM
- Opens the APM dashboard (mocked for demo)
- Sees: **"ACME web app - App Health Dashboard"**
- Views app health data, service metrics, and open alerts

**2. User identifies critical alert**
- Dashboard displays active alerts in a grid layout
- Alert example: "Database Cluster Connection Issues" (P1)
- User clicks on the alert card

**3. User triggers SREnity analysis**
- User clicks three-dot menu (⋮) on the alert
- Selects **"Analyze with SREnity"** option
- This initiates the automated analysis workflow

**4. SREnity gathers context (mocked for demo)**
- SREnity automatically pulls:
  - **Logs** from connected log system (mocked)
  - **Metrics** from monitoring system (mocked)
  - **Alert metadata** (title, severity, affected services, timestamp)

**5. SREnity performs Root Cause Analysis (REAL)**
- LangGraph-based RCA agent analyzes:
  - Log patterns and error messages
  - Metric anomalies and trends
  - Alert correlations
- Agent identifies root cause (real analysis)
- Generates RCA summary with findings

**6. SREnity retrieves runbooks (REAL)**
- Uses RCA findings as search context
- Queries runbook knowledge base with:
  - Root cause description
  - Affected service/component
  - Error patterns identified
- Advanced retrieval system (Ensemble: Vector + BM25 + Reranker) finds relevant procedures
- Retrieves step-by-step troubleshooting runbooks

**7. SREnity presents results (REAL)**
- Displays comprehensive analysis view:
  - **Root Cause Summary** - What went wrong and why
  - **Recommended Runbook Procedures** - Step-by-step resolution guidance
  - **Contextual Insights** - Why these procedures are relevant
- Optionally streams results for real-time feedback (non-streaming for demo)

---

## 🏗️ Technical Architecture

### Frontend (React + TypeScript)
- **APM Dashboard UI** - Mocked services, alerts, and metrics visualization
- **Modern dark theme** with glassmorphism effects
- **Responsive alert cards** in grid layout
- **Services table** with metrics, sparklines, and status indicators
- **Three-dot menu** for actions (Analyze with SREnity)

### Backend (FastAPI)
- **RCA Agent** - LangGraph-based log and metrics analyzer
- **Runbook RAG System** - Ensemble retriever with advanced retrieval
- **API Endpoints**:
  - `/api/alerts/{alert_id}/analyze` - Trigger analysis
  - `/api/services/{service_id}/analyze` - Service-level analysis
  - `/api/analysis/{analysis_id}/status` - Check analysis status
  - `/api/analysis/{analysis_id}/results` - Get analysis results

### Data Flow
```
Alert Selection
    ↓
Context Gathering (logs, metrics, metadata) [MOCKED]
    ↓
RCA Agent Analysis [REAL - LangGraph]
    ↓
Runbook RAG Search [REAL - Ensemble Retriever]
    ↓
Results Presentation [REAL]
```

---

## 🔧 What's Real vs Mocked

### **MOCKED (for demo)**
- APM dashboard data (services, alerts, metrics)
- Log data retrieval (simulated log system)
- Metrics data retrieval (simulated monitoring system)
- Alert metadata (static alert definitions)

### **REAL (functional)**
- RCA agent analysis (LangGraph-based)
- Root cause identification and summarization
- Runbook knowledge base (GitLab runbooks)
- Ensemble retrieval system (Vector + BM25 + Reranker)
- Runbook relevance scoring and ranking
- Step-by-step procedure retrieval
- Results generation and presentation

---

## 📋 Demo Flow Checklist

### Setup
- [ ] Start FastAPI backend server
- [ ] Start React frontend dev server
- [ ] Ensure runbook knowledge base is loaded
- [ ] Verify RCA agent is initialized
- [ ] Check mock data is available

### Demo Steps
1. **Show APM Dashboard**
   - Navigate to dashboard
   - Highlight active alerts
   - Show service health metrics

2. **Select Alert**
   - Click on a P1 alert (e.g., "Database Cluster Connection Issues")
   - Show alert details

3. **Trigger Analysis**
   - Click three-dot menu
   - Select "Analyze with SREnity"
   - Show loading/analysis state

4. **Display Results**
   - Show RCA summary (root cause identified)
   - Show retrieved runbook procedures
   - Explain why these procedures are relevant
   - Highlight step-by-step resolution guidance

5. **Demonstrate Value**
   - Compare: Manual runbook search vs SREnity automated analysis
   - Show time saved (from minutes to seconds)
   - Highlight contextual relevance

---

## 🎯 Key Messages

### Problem Statement
- SREs waste critical time searching runbooks during incidents
- Manual search is slow, fragmented, and context-missing
- Extended MTTR increases business impact

### Solution Value
- **Automated RCA** - Identifies root cause from logs/metrics automatically
- **Intelligent Runbook Retrieval** - Finds relevant procedures instantly
- **Contextual Guidance** - Provides step-by-step resolution based on actual incident
- **Reduced MTTR** - Faster incident resolution

### Technical Highlights
- **Advanced Retrieval** - Ensemble approach (Vector + BM25 + Reranker)
- **Agentic Reasoning** - LangGraph ReAct pattern for autonomous analysis
- **Production-Ready** - Scalable architecture with real runbook data
- **Extensible** - Foundation for full infrastructure stack coverage

---

## 🚀 Future Vision

This demo showcases the foundation for a comprehensive SRE assistant that will:
- Support all infrastructure components (Redis, Elasticsearch, Cloud SQL, CI/CD, etc.)
- Integrate with real APM and log aggregation systems
- Provide proactive monitoring and alerting recommendations
- Enable automated remediation workflows
- Scale to enterprise-level incident management

---

## 📝 Notes for Demo

- **Duration**: ~5 minutes
- **Focus**: Show end-to-end workflow from alert to resolution guidance
- **Emphasize**: Automation, speed, and contextual relevance
- **Highlight**: Real AI-powered analysis (not just scripted responses)
- **Demonstrate**: How RCA findings inform runbook retrieval

---

## 🔗 Related Documentation

- **Certification Report**: `certification-challenge-report.md` - Original RAG evaluation and metrics
- **Frontend README**: `frontend/README.md` - React frontend setup and structure
- **Project README**: `README.md` - Overall project overview and architecture

