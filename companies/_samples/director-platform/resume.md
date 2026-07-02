# Rohit Verma

Bengaluru, India | rohitatiit@gmail.com | +91 99888 44215
linkedin.com/in/rohit-verma-24084718 | github.com/rverma-dev

Director-level platform engineering leader for multi-tenant cloud, observability,
AI infrastructure, and governed agentic products. Built and operated 0->1
systems at scale, including $240M/month payments infrastructure, approximately
$6M annualized observability cost reduction, and enterprise SaaS platforms on
Salesforce Hyperforce. Led engineering organizations up to 40 engineers and a
30-person DevOps/SRE group, while owning architecture, execution quality, and
cross-team technical direction.

## Experience

### Principal Engineer (PMTS), MuleSoft (Salesforce)

Bengaluru, India; remote US org | Feb 2025 - Present

Founding engineer for multi-tenant observability, agent federation, and agentic
developer systems on Salesforce Hyperforce. Director-role positioning: platform
strategy, cross-team architecture, reliability economics, and governed AI
execution systems.

#### Anypoint Monitoring Alerts - Hyperforce re-platform + intelligent alerting

- Led architecture for a revenue-critical observability migration of 3M alerts
  from legacy InfluxDB to Amazon Managed Prometheus; delivered approximately
  80% cost-to-serve reduction, approximately $6M annualized, with zero
  customer-visible SLO regression.
- Designed multi-tenant alert evaluation for 50K-100K concurrent evaluations at
  P99 < 1s across at least 2 regions with blue-green deploys.
- Scaled platform operations to 60+ AMP workspaces and 45K alerts per workspace
  across enterprise tenants.
- Drove AU, UK, and GIA2H Hyperforce rollout work across app and infrastructure
  repositories, including new-FI onboarding automation, LaunchDarkly Relay Proxy
  support, and GIA-mode deployment wiring.
- Established execution-quality mechanisms: TEST_SCENARIOS manifests, APIM local
  firing harnesses, Bruno coverage, and a coherence-validator agent to keep
  RFCs, tests, and implementation aligned.
- Authored a 15-RFC architecture series across adjacent teams; designed
  PromQL-native anomaly detection with z-score and robust bands, 26h smoothing,
  persistence gates, and explainable dynamic thresholds.

#### Proactive Diagnostics / MuleSoft Pulse - AM Agent Federation

- Authored HLDs and ADRs for AM agent federation: MCP-first tool facades, A2A
  delegation, xAPI model gateway integration, LangGraph workflow contracts,
  memory/RAG boundaries, and workload isolation.
- Designed a governed diagnostic evidence plane that turns alert events into
  cited AI diagnoses over DIAF, app logs, metrics, traces, and KB/RAG without
  exposing raw archives, full logs, heap dumps, or tenant content to prompts.
- Converted passive alerting into proactive-diagnosis architecture for 160K
  alerts/week, with alert-storm dedup, per-tenant budgets, 5% runtime-overhead
  cap, source references, degradation flags, and audit/cost controls.

#### Internal IDE, Unleash

- Built an internal IDE for agent-assisted engineering across repo, ticket, PR,
  terminal, browser, automation, and agent context in one local-first workspace.
- Architected a four-plane multi-agent decision system: Knowledge, Decision
  Graph, Tiered Memory, and Governance, with 11 typed agents, A2A AgentCards,
  run ledger, path-tiered write authority, compliance hooks, repair detection,
  and outcomes review.
- Built Unleash, a local-first AI engineering IDE from a Superset fork with
  isolated git worktrees, terminal/chat/file/diff/browser/PR/GUS context,
  autonomous and coordinator workspaces, automations, and A2UI reports.

### Vice President / GSL - PaaS, Brane Enterprise

Bengaluru, India | Jan 2021 - Jul 2023

- Architected and delivered the full enterprise SaaS platform: control plane,
  tenancy, metering, telemetry, billing, and on-prem distribution for a
  MuleSoft-class integration platform.
- Built the infrastructure, platform, and security stack with a 2-engineer core,
  achieving enterprise-scale deployment and compliance readiness.
- Led a 30-person DevOps + SRE organization across CI/CD, observability, IaC,
  cost, incident response, and security.
- Delivered sidecar event-billing at 10M events/min with per-tenant rate
  limiting; tuned workflow engine to 10M TPS across Kafka, DynamoDB, TiDB, and
  Redis.
- Shipped NSL SaaS Accelerator with just-in-time IaC reused across Entity Store,
  Tag Manager, Event Manager, and Schedulers.
- Delivered full on-prem distribution on Nutanix, ScyllaDB, Kafka, TiDB, and
  ClickHouse; built entity data pipeline on ClickHouse, Redis, Kafka Connect,
  Glue, and S3.

### Principal Architect, Jupiter Money

Bengaluru, India | Nov 2019 - Jan 2021

- Single technical owner for ISO 27001, SOC 2, PCI-DSS, NPCI, UPI SAR
  compliance and partner-bank audits; all passed.
- Designed hub-and-spoke partner-bank architecture securing card and UPI
  transactions at $240M/month.
- Built in-house SIEM processing 200 GB/hour on OpenSearch with anomaly
  detection on banking logs.
- Built multi-tenant cloud-data platform on AWS, EMR, Airflow, Flink, and
  Kubernetes.

### Principal Architect, Niki.ai

Bengaluru, India | Dec 2017 - Nov 2019

- Led 3 EMs and 40 engineers; delivered Payment SDK handling 1.2M
  transactions/day for B2B partners.
- Built Dynamo-streams-based order fulfillment on CQRS and event sourcing.
- Replaced manual promotion engine with self-serve Kie rules engine; delivered
  PCI-DSS multi-account cloud infrastructure.

### Selected Earlier Experience

- Independent Consultant: redesigned a platform from 20K to 100K QPS; rebuilt
  RBAC/ABAC checks from 25 s to < 5 ms at 100K QPS; introduced tenant-context
  sidecar architecture and FinOps practices.
- Atlassian: led Jira data-migration integration frameworks for external
  sources across cross-functional teams; shipped Confluence image ALT-text
  generation using LAVIS/InstructBLIP.
- Sprinklr: shipped Integration Marketplace V1 with Consul-based discovery and
  Pubsubhubbub lifecycle management; led V1 customer trial with SAP C4C.
- Rokitt: built personalized travel platform with 200+ endpoints and data
  pipelines on Spark, Spark ML, Redis, and Databricks.

## Education

B.Tech (Hons), Indian Institute of Technology Kharagpur | Jul 2007 - May 2011

## Skills

- Leadership: org design, manager mentorship, RFC culture, executive
  communication, cross-team architecture, incident response, delivery quality.
- AI & Agent Systems: multi-agent orchestration, MCP/A2A contracts, LangGraph,
  Spring AI, governance substrates, RAG, vector search, LLM evaluation.
- Platform & Infra: AWS, Kubernetes/EKS, Istio, Cilium, Spinnaker, Argo
  Rollouts, GitHub Actions, Terraform/CDK, Nutanix.
- Data & Streaming: Kafka, Flink, ClickHouse, TiDB, ScyllaDB, Cassandra, Redis,
  Hudi, DynamoDB, Druid, Amazon Managed Prometheus.
- Observability & Security: OpenTelemetry, Grafana, Prometheus/PromQL, K6,
  OpenSearch, SIEM, anomaly detection, PCI-DSS, SOC 2, ISO 27001, IAM.
- Languages: Go, Python, TypeScript, Java.
