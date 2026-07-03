---
layout: resume
title: Rohit Verma - American Express - Director Software Engineering Resume
permalink: /applications/resumes/app-20260702-american-express-director-software-engineering-dc7520e5/submitted/
---
# Rohit Verma

Bengaluru, India | rohitatiit@gmail.com | +91 99888 44215
linkedin.com/in/rohit-verma-24084718 | github.com/rverma-dev

Position around regulated financial infrastructure, enterprise data pipelines, cloud-native delivery, and leading large engineering/SRE organizations.
Built and operated 0->1 systems at scale including $240M/month payments infrastructure, approximately $6M annualized observability cost reduction, and enterprise-grade SaaS systems on Salesforce Hyperforce.

## Experience

### Principal Engineer (PMTS), MuleSoft (Salesforce)

Bengaluru, India; remote US org | Feb 2025 - Present

Founding engineer (0->1) for multi-tenant observability, agent federation, and
agentic developer systems on Salesforce Hyperforce. Owns architecture, RFCs, and
cross-team technical direction.

#### Anypoint Monitoring Alerts - Hyperforce re-platform + intelligent alerting

- Migrated 3M alerts off legacy InfluxDB onto Amazon Managed Prometheus in phased rollout; delivered approximately 80% cost-to-serve reduction, approximately $6M annualized, with zero customer-visible SLO regression.
- Multi-tenant alert evaluation platform handling 50K-100K concurrent evaluations at P99 < 1s across at least 2 regions with blue-green deploys.
- Scaled to 60+ AMP workspaces and 45K alerts per workspace across enterprise tenants.
- Drove AU, UK, and GIA2H Hyperforce rollout work across app and infra repos, including new-FI onboarding automation, LaunchDarkly Relay Proxy support, and GIA-mode deployment wiring.
- Introduced TEST_SCENARIOS manifests, APIM local firing harnesses, Bruno coverage, and a coherence-validator agent to keep RFCs, tests, and implementation aligned.
- Designed core platform primitives: tenant sharding, rule sync, buffering, distributed scheduling, and APIM alert migration paths.
- Authored a 15-RFC series shaping observability architecture across adjacent teams; designed PromQL-native anomaly detection with z-score / robust bands, 26h smoothing, persistence gates, and explainable dynamic thresholds.

#### Anypoint Visualizer - Hyperforce re-platform + Druid-native topology

- Scales to 10,000+ concurrent orgs, approximately 15M applications, and approximately 50M edges, ingesting 500K-1M events/min at peak.
- Less than 5-minute topology freshness SLO via watermark-based incremental graph construction over Druid.
- Simplified architecture: replaced Logstash with Druid-native ingestion; consolidated visualizer-janitor into visualizer-topology-processor via Kubernetes leader election.

#### Proactive Diagnostics / MuleSoft Pulse - AM Agent Federation

- Authored HLD/ADRs for AM agent federation across existing omni/platform surfaces: MCP-first tool facades, A2A delegation path, xAPI model gateway integration, LangGraph workflow contracts, memory/RAG boundaries, and workload isolation.
- Designed a governed diagnostic evidence plane that turns alert events into cited AI diagnoses over DIAF, app logs, metrics, traces, and KB/RAG without exposing raw archives, full logs, heap dumps, or tenant content to prompts.
- Converted passive alerting into a proactive-diagnosis product architecture for 160K alerts/week, with alert-storm dedup, per-tenant budgets, 5% runtime-overhead cap, source references, degradation flags, and audit/cost controls.

#### Internal IDE, Unleash

- Built an internal IDE for agent-assisted engineering: repo, ticket, PR, terminal, browser, automation, and agent context in one local-first workspace.
- Architected a four-plane multi-agent decision system: Knowledge, Decision Graph, Tiered Memory, and Governance, with 11 typed agents, A2A AgentCards, run ledger, path-tiered write authority, compliance hooks, repair detection, and outcomes review.
- Built Unleash, a local-first AI engineering IDE from a Superset fork: isolated git worktrees, terminal/chat/file/diff/browser/PR/GUS context, autonomous and coordinator workspaces, automations, and structured A2UI reports.
- Created the Unleash distribution surface with product docs, stable/canary electron-updater feeds, DMG release assets, branch-backed GitHub Enterprise Pages publishing, and unauthenticated download verification.

### Independent Consultant

Bengaluru, India | Mar 2024 - Feb 2025

- Brandshark: low-latency GenAI video pipeline - chapterization, semantic search, content repurposing.
- DRDO Radar Unit: flight-simulation system with synthetic data generation and MIL/video data integration.
- Gaian Solutions: platform redesign - scaled 20K -> 100K QPS; rebuilt RBAC/ABAC reducing permission checks from 25 s -> < 5 ms at 100K QPS; introduced tenant-context sidecar architecture and cloud FinOps practices.

### Senior Software Engineer, Atlassian

Bengaluru, India | Aug 2023 - Mar 2024

- Led JIRA data-migration integration frameworks for external sources across multiple cross-functional teams.
- Shipped an ALT-text generator for Confluence images using LAVIS, an InstructBLIP variant.

### Vice President / GSL - PaaS, Brane Enterprise

Bengaluru, India | Jan 2021 - Jul 2023

- Architected and delivered the full enterprise SaaS platform: control plane, tenancy, metering, telemetry, billing, and on-prem distribution, a MuleSoft-class integration platform for enterprise customers.
- Built the entire infrastructure, platform, and security stack with a 2-engineer team, achieving enterprise-scale deployment and compliance readiness.
- NSL SaaS Accelerator with just-in-time IaC, reused across Entity Store, Tag Manager, Event Manager, and Schedulers.
- Sidecar event-billing at 10M events/min with per-tenant rate limiting; workflow engine tuned to 10M TPS across Kafka, DynamoDB, TiDB, and Redis.
- Full on-prem distribution on Nutanix, ScyllaDB, Kafka, TiDB, and ClickHouse; entity data pipeline on ClickHouse, Redis, Kafka Connect, Glue, and S3.
- Led a 30-person DevOps + SRE organization across CI/CD, observability, IaC, cost, incident response, and security.
- Global search on vector embeddings + Elasticsearch for semantic, faceted, typeahead, and fuzzy search.

### Principal Architect, Jupiter Money

Bengaluru, India | Nov 2019 - Jan 2021

- Single technical owner for ISO 27001, SOC 2, PCI-DSS, NPCI, UPI SAR compliance and partner-bank audits; all passed.
- Hub-and-spoke architecture with partner banks securing all card and UPI transactions at $240M/month.
- In-house SIEM processing 200 GB/hour on OpenSearch with anomaly detection on banking logs.
- Multi-tenant cloud-data platform on AWS, EMR, Airflow, Flink, and Kubernetes.

### Principal Architect, Niki.ai

Bengaluru, India | Dec 2017 - Nov 2019

- Led 3 EMs and 40 engineers; Payment SDK handling 1.2M transactions/day for B2B partners.
- Dynamo-streams-based order fulfillment on CQRS and event sourcing.
- Replaced manual promotion engine with self-serve Kie rules engine; PCI-DSS multi-account cloud infrastructure.

### Lead Product Engineer, Sprinklr

Bengaluru, India | Jul 2017 - Dec 2017

- Architected and shipped Integration Marketplace V1 with Consul-based discovery and Pubsubhubbub lifecycle management; led V1 customer trial with SAP C4C.

### Senior Software Engineer, Rokitt

Bengaluru, India / New Jersey | May 2015 - Jul 2017

- Personalized travel platform with 200+ endpoints and third-party integrations.
- Large-scale data pipelines on Spark, Spark ML, Redis, and Databricks.
- Conceptualized and shipped Genesis, a synthetic-data generator that evolved into a commercial product for a Boston Consulting acquisition validation engagement.

### Earlier Experience

May 2011 - Mar 2015

- Sr. Software Engineer, QA Source (Bebo Technologies): refactored e-commerce platform for multi-tenancy; SOA and Elasticsearch analytics.
- Software Engineer, Mphasis (HP): core-banking APIs, SWIFT-over-JMS/MQTT bridge, and SOAP services for Symantec Norton Store.

## Education

B.Tech (Hons), Indian Institute of Technology Kharagpur | Jul 2007 - May 2011

## Skills

- AI & Agent Systems: multi-agent orchestration, MCP / A2A contracts, LangGraph, Spring AI, governance substrates, RAG, vector search, LLM evaluation, compliance gating, OpenAI / Anthropic SDKs.
- Platform & Infra: AWS, Kubernetes / EKS, Istio, Cilium, Spinnaker, Argo Rollouts, GitHub Actions, Terraform / CDK, Nutanix.
- Data & Streaming: Kafka, Flink, KSQLDB, ClickHouse, TiDB, ScyllaDB, Cassandra, Redis, Hudi, DynamoDB, Druid, Amazon Managed Prometheus.
- Observability & SRE: OpenTelemetry, Grafana, Prometheus / PromQL, K6, OpenSearch, custom SIEM, anomaly detection, blue-green and canary rollouts.
- Security & Compliance: zero trust, PCI-DSS, SOC 2, ISO 27001, NPCI / UPI SAR, Keycloak, IAM design.
- Languages: Go, Python, TypeScript, Java.
