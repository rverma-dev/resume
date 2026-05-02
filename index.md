---
layout: default
title: Rohit Verma — Resume
---

# Rohit Verma

Bengaluru, India | [rohitatiit@gmail.com](mailto:rohitatiit@gmail.com) | [+91 99888 44215](tel:+919988844215)<br>
[linkedin.com/in/rohit-verma-24084718](https://www.linkedin.com/in/rohit-verma-24084718) | [github.com/rverma-dev](https://github.com/rverma-dev)

## Summary

Principal-level engineer with 15 years building multi-tenant control planes, observability platforms, payment infrastructure, and governed AI agent systems. Owns 0-to-1 architecture from RFCs through production operations, with outcomes including **$240M/month payments infrastructure**, **~$6M annualized platform cost reduction**, and SaaS platforms running at enterprise scale. Currently focused on AI control-plane primitives: memory, authority, governance, compliance, and production-grade multi-agent decision systems.

## Core Expertise

Multi-tenant control planes · observability & telemetry (OpenTelemetry, Prometheus, Elastic) · AI agent systems & decision intelligence · distributed systems (Kafka, ClickHouse, Flink, OpenSearch, Druid) · cloud & Kubernetes platforms (AWS, EKS, FinOps) · security & compliance (SOC 2, PCI-DSS, ISO 27001, NPCI) · platform governance, reliability & cost optimization · engineering leadership and cross-org influence.

## Experience

**Principal MTS, MuleSoft (Salesforce)** | Bengaluru, India; remote US org | Feb 2025 – Present

Founding engineer (0→1) for multi-tenant observability platforms on Salesforce Hyperforce. Owns architecture, RFCs, and cross-team technical direction.

*Anypoint Monitoring Alerts — Hyperforce re-platform*

- Migrated **3M alerts** off legacy InfluxDB onto Amazon Managed Prometheus in phased rollout; delivered **~80% cost-to-serve reduction (~$6M annualized)** with zero customer-visible SLO regression.
- Multi-tenant alert evaluation platform handling **50K–100K concurrent evaluations** at **P99 < 1s** across ≥2 regions with blue-green deploys.
- Scaled to **60+ AMP workspaces** and **45K alerts per workspace** with tenant sharding, outbox rule sync, reorder buffering, SQS FIFO sync, leader-election scheduling, VegaCache, and 9-tier SKU quotas.
- Authored a 15-RFC series now shaping observability architecture across adjacent teams.

*Anypoint Visualizer — Hyperforce re-platform + Druid-native topology*

- Scales to **10,000+ concurrent orgs**, **~15M applications**, and **~50M edges**, ingesting **500K–1M events/min** at peak.
- **< 5-minute topology freshness SLO** via watermark-based incremental graph construction over Druid.
- Simplified architecture: replaced Logstash with Druid-native ingestion; consolidated `visualizer-janitor` into `visualizer-topology-processor` via k8s leader election.

**Governed Multi-Agent Systems — Side Work (own time, open source)** | 2024 – Present

- Built a **four-plane multi-agent decision system** (Knowledge / Decision Graph / Tiered Memory / Governance) on Claude Code hooks — the control-plane layer most agent projects never ship.
- **11 typed agents with A2A AgentCards**, SQLite run ledger, path-tiered write authority, LLM compliance gate via PreToolUse hook, repair-detection loop, and daily outcomes-review cron.
- Tiered agent memory (episodic / semantic / heuristics / assumptions with expiry / rejected) aligned to cognitive-architecture patterns rather than a flat store.
- Recognized internally (**top-20 across MuleSoft**) for AI leverage — measured on token-to-value, not consumption.

**Independent Consultant** | Bengaluru, India | Mar 2024 – Feb 2025

- **Brandshark:** low-latency GenAI video pipeline — chapterization, semantic search, content repurposing.
- **DRDO Radar Unit:** flight-simulation system with synthetic data generation and MIL/video data integration.
- **Gaian Solutions:** platform redesign — scaled **20K → 100K QPS**; rebuilt RBAC/ABAC reducing permission checks from **25 s → < 5 ms** at 100K QPS; introduced tenant-context sidecar architecture and cloud FinOps practices.

**Senior Software Engineer, Atlassian** | Bengaluru, India | Aug 2023 – Mar 2024

- Led JIRA data-migration integration frameworks for external sources across multiple cross-functional teams.
- Shipped an ALT-text generator for Confluence images using LAVIS (InstructBLIP variant).

**Vice President / GSL — PaaS, Brane Enterprise** | Bengaluru, India | Jan 2021 – Jul 2023

- Architected and delivered the full enterprise SaaS platform — control plane, tenancy, metering, telemetry, billing, on-prem distribution — a **MuleSoft-class integration platform** for enterprise customers.
- **Built the entire internal infrastructure and security platform** — AWS + EKS + GitHub Actions + Spinnaker + Argo Rollouts, Wazuh-based SIEM, continuous-compliance automation; passed all target compliance audits.
- NSL SaaS Accelerator with **just-in-time IaC**, reused across Entity Store, Tag Manager, Event Manager, and Schedulers.
- Sidecar event-billing at **10M events/min** with per-tenant rate limiting; workflow engine tuned to **10M TPS** across Kafka, DynamoDB, TiDB, and Redis.
- Full on-prem distribution on Nutanix, ScyllaDB, Kafka, TiDB, and ClickHouse; entity data pipeline on ClickHouse, Redis, Kafka Connect, Glue, and S3.
- Led a **30-person DevOps + SRE organization** across CI/CD (Flux), observability (GLTM), IaC, cost, incident response (Opsgenie + PagerDuty), security.
- Global search on vector embeddings + Elasticsearch (semantic, faceted, typeahead, fuzzy).

<div class="page-break"></div>

**Principal Architect, Jupiter Money** | Bengaluru, India | Nov 2019 – Jan 2021

- **Single technical owner** for ISO 27001, SOC 2, PCI-DSS, NPCI, UPI SAR compliance and partner-bank audits — all passed.
- Hub-and-spoke architecture with partner banks securing all card + UPI transactions at **$240M/month**.
- In-house **SIEM processing 200 GB/hour** on OpenSearch with anomaly detection on banking logs.
- Multi-tenant cloud-data platform on AWS + EMR + Airflow + Flink + Kubernetes.

**Principal Architect, Niki.ai** | Bengaluru, India | Dec 2017 – Nov 2019

- Led **3 EMs + 40 engineers**; Payment SDK handling **1.2M transactions/day** for B2B partners.
- Dynamo-streams-based order fulfillment on CQRS + event sourcing.
- Replaced manual promotion engine with self-serve Kie rules engine; PCI-DSS multi-account cloud infrastructure.

**Lead Product Engineer, Sprinklr** | Bengaluru, India | Jul 2017 – Dec 2017

- Architected and shipped **Integration Marketplace V1** with Consul-based discovery and Pubsubhubbub lifecycle management; led V1 customer trial with SAP C4C.

**Senior Software Engineer, Rokitt** | Bengaluru, India / New Jersey | May 2015 – Jul 2017

- Personalized travel platform with **200+ endpoints** and third-party integrations (TripAdvisor et al.).
- Large-scale data pipelines on Spark / Spark ML / Redis / Databricks.
- Conceptualized and shipped **Genesis** — a synthetic-data generator that evolved into a commercial product (Boston Consulting acquisition validation engagement).

**Earlier Experience** | May 2011 – Mar 2015

- **Sr. Software Engineer, QA Source (Bebo Technologies):** refactored e-commerce platform for multi-tenancy; SOA + ES analytics.
- **Software Engineer, Mphasis (HP):** core-banking APIs, SWIFT-over-JMS/MQTT bridge, SOAP services for Symantec Norton Store.

## Writing & Open Source

- **GitHub:** [github.com/rverma-dev](https://github.com/rverma-dev)
- **Technical writing:** multi-agent systems, observability, platform architecture *(articles in progress)*

## Education

**B.Tech (Hons), Indian Institute of Technology Kharagpur** | Jul 2007 – May 2011

## Skills

**AI & Agent Systems:** multi-agent orchestration, Claude Code hooks, A2A contracts, governance substrates, RAG, LangChain / LangGraph, vector search, LLM evaluation, compliance gating, OpenAI / Anthropic SDKs.<br>
**Platform & Infra:** AWS, Kubernetes / EKS, Istio, Cilium, Spinnaker, Argo Rollouts, GitHub Actions, Terraform / CDK, Nutanix.<br>
**Data & Streaming:** Kafka, Flink, KSQLDB, ClickHouse, TiDB, ScyllaDB, Cassandra, Redis, Hudi, DynamoDB, Druid, Amazon Managed Prometheus.<br>
**Observability & SRE:** OpenTelemetry, Grafana, Prometheus, K6, OpenSearch, custom SIEM, blue-green and canary rollouts.<br>
**Security & Compliance:** zero trust, PCI-DSS, SOC 2, ISO 27001, NPCI / UPI SAR, Keycloak, IAM design.<br>
**Languages:** Go, Python, TypeScript, Java.
