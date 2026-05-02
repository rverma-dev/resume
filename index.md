# Rohit Verma

<span class="iconify" data-icon="tabler:brand-linkedin"></span> [LinkedIn](https://www.linkedin.com/in/rohit-verma-24084718)
  : <span class="iconify" data-icon="tabler:brand-github"></span>  [gh/rverma-dev](https://github.com/rverma-dev)
  : <span class="iconify" data-icon="tabler:phone"></span> [(+91) 9988844215](https://wa.me/11234567890)

<span class="iconify" data-icon="ic:outline-location-on"></span> Bengaluru, India &nbsp;•&nbsp; Open to global / remote roles
  : <span class="iconify" data-icon="tabler:mail"></span> [rohitatiit@gmail.com](mailto:rohitatiit@gmail.com)

## Summary

Principal-level engineer specializing in multi-tenant control planes, observability platforms, and governed AI agent systems. Track record of building 0→1 production systems at scale with small teams and driving measurable business outcomes.

Delivered platform systems powering:

- $240M/month payments infrastructure (Jupiter)
- MuleSoft-class SaaS platform (Brane)
- Multi-tenant observability systems on Salesforce Hyperforce (MuleSoft)

Recently focused on AI control-plane primitives — memory, authority, governance, and compliance — enabling production-grade multi-agent decision systems.

## CORE EXPERTISE
- Multi-tenant control planes & platform architecture
- Observability & telemetry systems (OpenTelemetry, Prometheus, Elastic)
- AI agent systems & decision intelligence platforms
- Distributed systems (Kafka, ClickHouse, Flink, OpenSearch)
- Cloud infrastructure (AWS, Kubernetes, EKS, FinOps)
- Security & compliance systems (SOC2, PCI-DSS, ISO27001)
- Platform governance, reliability & cost optimization
- Engineering leadership & cross-org influence

## Experience

**Principal Engineer (MTS), MuleSoft — Salesforce**
  : **Bengaluru — remote, US Org**  
  : **Feb 2025 – Present**

Founding engineer (0→1) for multi-tenant observability platforms on Salesforce Hyperforce. Owns architecture, RFCs, and cross-team technical direction.

*Anypoint Monitoring Alerts (Hyperforce re-platform):*
- Migrated **3M alerts** off legacy InfluxDB onto Amazon Managed Prometheus (AMP) in multiple phases; delivered **~80% cost-to-serve reduction (~$6M annualized)** with zero customer-visible SLO regression.
- Built a multi-tenant alert evaluation platform handling 50K–100K concurrent evaluations with P99 <1s latency across multi-region deployments
- Scaled to 60+ workspaces / 45K alerts per workspace, supporting high-density enterprise tenants
- Designed platform primitives including tenant sharding, outbox-based rule sync, reorder buffering, and distributed scheduler coordination
- Authored and drove adoption of platform RFCs as a base of Spec driven development influencing observability architecture across teams

*Anypoint Visualizer (Hyperforce re-platform + Druid-native topology):*
- Built topology system supporting 10K+ orgs, 15M+ applications, and ~50M edges, ingesting 500K–1M events/min
- Achieved <5-minute topology freshness SLO using incremental graph construction and watermark-based processing
- Simplified architecture by replacing Logstash dependencies with Druid-native ingestion pipelines

**Side Work (own time, internal open source) — Governed Multi-Agent Systems**
  : **2024 – Present**

- Built a **four-plane multi-agent decision system** (Knowledge / Decision Graph / Tiered Memory / Governance) on Claude Code hooks — the control-plane layer most agent projects never ship.
- **11 typed agents with A2A AgentCards** (self-describing inputs / outputs / consumers), **SQLite run ledger**, **path-tiered write authority** (observe → recommend → draft_decision → publish), **LLM compliance gate via PreToolUse hook**, repair detection loop, and a daily outcomes-review cron.
- Tiered agent memory (episodic / semantic / heuristics / assumptions / rejected) aligned to cognitive-architecture patterns rather than a single flat store.
- Recognized internally (top 20 across MuleSoft) for AI leverage — measured on token-to-value, not consumption.

**Independent Consultant**
  : **Bengaluru (KA)**  
  : **Mar 2024 – Feb 2025**

- Designed a low-latency GenAI video processing system for **Brandshark** (chapterization, semantic search, content repurposing).
- Built flight simulation for **DRDO Radar Unit** — synthetic data generation + MIL/video data integration.
- Consultant for redesign **Gaian Solutions Platform**: scaled from **20K → 100K QPS**, rebuilt RBAC/ABAC reducing permission checks from **25s → <5ms at 100K QPS**, introduced tenant-context sidecar architecture and cloud FinOps practices.

**Senior Software Engineer, Atlassian**
  : **Bengaluru (KA)**  
  : **Aug 2023 – Mar 2024**

- Led JIRA data-migration integration frameworks for external sources across multiple cross-functional teams.
- Shipped an ALT-text generator for Confluence images using LAVIS (InstructBLIP variant).

**Vice President / GSL — PaaS, Brane Enterprise**
  : **Bengaluru (KA)**  
  : **Jan 2021 – July 2023**

- Architected and delivered the full enterprise SaaS platform — control plane, tenancy, metering, telemetry, billing, on-prem distribution — a **MuleSoft-class integration platform** for enterprise customers.
- **Built the entire internal infrastructure stack and security platform**: AWS + EKS + GitHub Actions + Spinnaker + Argo Rollouts, Wazuh-based SIEM, continuous-compliance automation. Passed all target compliance audits with that two-person team.
- NSL SaaS Accelerator with **just-in-time IaC** enabling concurrent tenant onboarding; reused across Entity Store, Tag Manager, Event Manager, Schedulers.
- Sidecar-based event billing scaling to **10M events/min** with per-tenant rate limiting; workflow engine tuned to **10M TPS** across Kafka / Dynamo / TiDB / Redis.
- Full on-prem suite for enterprise (Nutanix, ScyllaDB, Kafka, TiDB, ClickHouse); entity data pipeline on ClickHouse + Redis + Kafka Connect + Glue + S3.
- Led a **30-person DevOps + SRE organization** across CI/CD (Flux), observability (GLTM), IaC, cost management, incident response (Opsgenie + PagerDuty), security.
- Global search on vector embeddings + Elasticsearch (semantic, faceted, typeahead, fuzzy).

**Principal Architect, Jupiter Money**
  : **Bengaluru (KA)**  
  : **Nov 2019 – Jan 2021**

- **Single technical owner** for ISO 27001, SOC 2, PCI-DSS, NPCI, UPI SAR compliance — plus partner-bank audits — all passed.
- Hub-and-spoke architecture with partner banks now securing **all card + UPI transactions at $240M/month**.
- In-house **SIEM processing 200GB/hour** on OpenSearch with anomaly detection on banking logs.
- Multi-tenant cloud-data platform on AWS + EMR + Airflow + Flink + Kubernetes.

**Principal Architect, Niki.ai**
  : **Bengaluru (KA)**  
  : **Dec 2017 – Nov 2019**

- Led **3 EMs + 40 engineers**; Payment SDK handling **1.2M transactions/day** for B2B partners.
- Dynamo-streams-based order fulfillment on CQRS + event sourcing.
- Replaced manual promotion engine with a self-serve Kie rules engine; PCI-DSS-compliant multi-account cloud infra.

**Lead Product Engineer, Sprinklr**
  : **Bengaluru (KA)**  
  : **Jul – Dec 2017**

- Architected and shipped **Integration Marketplace V1** with a Consul-based discovery layer and Pubsubhubbub lifecycle management; led V1 customer trial with SAP C4C.

**Senior Software Engineer, Rokitt**
  : **Bengaluru (KA) / New Jersey**  
  : **May 2015 – Jul 2017**

- Built a personalized travel platform with **200+ endpoints** and third-party integrations (TripAdvisor et al.).
- Engineered large-scale data pipelines on Spark / Spark ML / Redis / Databricks.
- Conceptualized and shipped **Genesis**, a synthetic-data generator that evolved into a commercial product (Boston Consulting engagement for acquisition validation).

**Earlier Experience**
  : **May 2011 – Mar 2015**

- **Sr. Software Engineer, QA Source (Bebo Technologies):** refactored e-commerce platform for multi-tenancy; SOA + ES analytics.
- **Software Engineer, Mphasis (HP):** core-banking APIs, SWIFT-over-JMS/MQTT bridge, SOAP services for Symantec Norton Store.

## Writing & Open Source

- **GitHub:** [github.com/rverma-dev](https://github.com/rverma-dev)
- **Technical writing:** multi-agent systems, observability, platform architecture *(articles in progress)*

## Education

**B.Tech (Hons), Indian Institute of Technology Kharagpur**
  : **Jul 2007 – May 2011**

## Skills

**AI & Agent Systems:** Multi-agent orchestration (Claude Code hooks, A2A contracts), governance substrates, RAG, LangChain / LangGraph, vector search (Milvus, Elasticsearch), LLM evaluation & compliance gating, OpenAI / Anthropic SDKs.

**Platform & Infra:** AWS, Kubernetes / EKS, Istio, Cilium, Spinnaker, Argo Rollouts, GitHub Actions, Terraform / CDK, Nutanix.

**Data & Streaming:** Kafka, Flink, KSQLDB, ClickHouse, TiDB, ScyllaDB, Cassandra, Redis, Hudi, DynamoDB, Druid, Amazon Managed Prometheus.

**Observability & SRE:** OpenTelemetry, Grafana, Prometheus, K6, OpenSearch, custom SIEM, blue-green & canary rollouts.

**Security & Compliance:** Zero-trust, PCI-DSS, SOC 2, ISO 27001, NPCI / UPI SAR, Keycloak, IAM design.

**Languages:** Go, Python, TypeScript, Java.
