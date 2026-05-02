---
layout: default
title: Rohit Verma — Resume
---

<p class="masthead"><strong class="name">Rohit Verma</strong> <span class="contact">Bengaluru, India | <a href="mailto:rohitatiit@gmail.com">rohitatiit@gmail.com</a> | <a href="tel:+919988844215">+91 99888 44215</a> | <a href="https://www.linkedin.com/in/rohit-verma-24084718">linkedin.com/in/rohit-verma-24084718</a> | <a href="https://github.com/rverma-dev">github.com/rverma-dev</a></span></p>

<div class="profile">
  <p class="intro">Principal engineer with 15 years building multi-tenant control planes, observability platforms, payment infrastructure, and governed AI agent systems. Owns 0-to-1 architecture from RFCs through production operations, with outcomes including <strong>$240M/month payments infrastructure</strong>, <strong>~$6M annualized platform cost reduction</strong>, and SaaS platforms running at enterprise scale.</p>
  <p class="expertise">Multi-tenant control planes · observability & telemetry (OpenTelemetry, Prometheus, Elastic) · AI agent systems & decision intelligence · distributed systems (Kafka, ClickHouse, Flink, OpenSearch, Druid) · cloud & Kubernetes platforms (AWS, EKS, FinOps) · security & compliance (SOC 2, PCI-DSS, ISO 27001, NPCI) · platform governance, reliability & cost optimization · engineering leadership and cross-org influence.</p>
</div>

## Experience

<div class="role">
  <strong>Principal Engineer(MTS), MuleSoft (Salesforce)</strong>
  <span>Bengaluru, India; remote US org | Feb 2025 – Present</span>
</div>

Founding engineer (0→1) for multi-tenant observability platforms on Salesforce Hyperforce. Owns architecture, RFCs, and cross-team technical direction.

<p class="project"><em>Anypoint Monitoring Alerts — Hyperforce re-platform</em></p>

- Migrated **3M alerts** off legacy InfluxDB onto Amazon Managed Prometheus in phased rollout; delivered **~80% cost-to-serve reduction (~$6M annualized)** with zero customer-visible SLO regression.
- Multi-tenant alert evaluation platform handling **50K–100K concurrent evaluations** at **P99 < 1s** across ≥2 regions with blue-green deploys.
- Scaled to **60+ AMP workspaces** and **45K alerts per workspace** with tenant sharding, outbox rule sync, reorder buffering, SQS FIFO sync, leader-election scheduling, VegaCache, and 9-tier SKU quotas.
- Authored a 15-RFC series now shaping observability architecture across adjacent teams.

<p class="project"><em>Anypoint Visualizer — Hyperforce re-platform + Druid-native topology</em></p>

- Scales to **10,000+ concurrent orgs**, **~15M applications**, and **~50M edges**, ingesting **500K–1M events/min** at peak.
- **< 5-minute topology freshness SLO** via watermark-based incremental graph construction over Druid.
- Simplified architecture: replaced Logstash with Druid-native ingestion; consolidated `visualizer-janitor` into `visualizer-topology-processor` via k8s leader election.

<p class="project"><em>AI Platform & Agent Systems (Strategic Initiative)</em></p>
- Designed and built a governed multi-agent decision system to augment product and engineering decision-making using real-time customer and internal signals
- Architected a **four-plane multi-agent decision system** (Knowledge / Decision Graph / Tiered Memory / Governance) — the control-plane layer most agent projects never ship.
- **11 typed agents with A2A AgentCards**, SQLite run ledger, path-tiered write authority, LLM compliance gate via PreToolUse hook, repair-detection loop, and daily outcomes-review cron.
- Tiered agent memory (episodic / semantic / heuristics / assumptions with expiry / rejected) aligned to cognitive-architecture patterns rather than a flat store.
- Established governance-first architecture (policy thresholds, risk gating, decision validation) enabling safe scaling of agent systems

<div class="role">
  <strong>Independent Consultant</strong>
  <span>Bengaluru, India | Mar 2024 – Feb 2025</span>
</div>

- **Brandshark:** low-latency GenAI video pipeline — chapterization, semantic search, content repurposing.
- **DRDO Radar Unit:** flight-simulation system with synthetic data generation and MIL/video data integration.
- **Gaian Solutions:** platform redesign — scaled **20K → 100K QPS**; rebuilt RBAC/ABAC reducing permission checks from **25 s → < 5 ms** at 100K QPS; introduced tenant-context sidecar architecture and cloud FinOps practices.

<div class="role">
  <strong>Senior Software Engineer, Atlassian</strong>
  <span>Bengaluru, India | Aug 2023 – Mar 2024</span>
</div>

- Led JIRA data-migration integration frameworks for external sources across multiple cross-functional teams.
- Shipped an ALT-text generator for Confluence images using LAVIS (InstructBLIP variant).

<div class="role">
  <strong>Vice President / GSL — PaaS, Brane Enterprise</strong>
  <span>Bengaluru, India | Jan 2021 – Jul 2023</span>
</div>

- Architected and delivered the full enterprise SaaS platform — control plane, tenancy, metering, telemetry, billing, on-prem distribution — a **MuleSoft-class integration platform** for enterprise customers.
- **Built the entire internal infrastructure and security platform** — AWS + EKS + GitHub Actions + Spinnaker + Argo Rollouts, Wazuh-based SIEM, continuous-compliance automation; passed all target compliance audits.
- NSL SaaS Accelerator with **just-in-time IaC**, reused across Entity Store, Tag Manager, Event Manager, and Schedulers.
- Sidecar event-billing at **10M events/min** with per-tenant rate limiting; workflow engine tuned to **10M TPS** across Kafka, DynamoDB, TiDB, and Redis.
- Full on-prem distribution on Nutanix, ScyllaDB, Kafka, TiDB, and ClickHouse; entity data pipeline on ClickHouse, Redis, Kafka Connect, Glue, and S3.
- Led a **30-person DevOps + SRE organization** across CI/CD (Flux), observability (GLTM), IaC, cost, incident response (Opsgenie + PagerDuty), security.
- Global search on vector embeddings + Elasticsearch (semantic, faceted, typeahead, fuzzy).

<div class="role">
  <strong>Principal Architect, Jupiter Money</strong>
  <span>Bengaluru, India | Nov 2019 – Jan 2021</span>
</div>

- **Single technical owner** for ISO 27001, SOC 2, PCI-DSS, NPCI, UPI SAR compliance and partner-bank audits — all passed.
- Hub-and-spoke architecture with partner banks securing all card + UPI transactions at **$240M/month**.
- In-house **SIEM processing 200 GB/hour** on OpenSearch with anomaly detection on banking logs.
- Multi-tenant cloud-data platform on AWS + EMR + Airflow + Flink + Kubernetes.

<div class="role">
  <strong>Principal Architect, Niki.ai</strong>
  <span>Bengaluru, India | Dec 2017 – Nov 2019</span>
</div>

- Led **3 EMs + 40 engineers**; Payment SDK handling **1.2M transactions/day** for B2B partners.
- Dynamo-streams-based order fulfillment on CQRS + event sourcing.
- Replaced manual promotion engine with self-serve Kie rules engine; PCI-DSS multi-account cloud infrastructure.

<div class="role">
  <strong>Lead Product Engineer, Sprinklr</strong>
  <span>Bengaluru, India | Jul 2017 – Dec 2017</span>
</div>

- Architected and shipped **Integration Marketplace V1** with Consul-based discovery and Pubsubhubbub lifecycle management; led V1 customer trial with SAP C4C.

<div class="role">
  <strong>Senior Software Engineer, Rokitt</strong>
  <span>Bengaluru, India / New Jersey | May 2015 – Jul 2017</span>
</div>

- Personalized travel platform with **200+ endpoints** and third-party integrations (TripAdvisor et al.).
- Large-scale data pipelines on Spark / Spark ML / Redis / Databricks.
- Conceptualized and shipped **Genesis** — a synthetic-data generator that evolved into a commercial product (Boston Consulting acquisition validation engagement).

<div class="role">
  <strong>Earlier Experience</strong>
  <span>May 2011 – Mar 2015</span>
</div>

- **Sr. Software Engineer, QA Source (Bebo Technologies):** refactored e-commerce platform for multi-tenancy; SOA + ES analytics.
- **Software Engineer, Mphasis (HP):** core-banking APIs, SWIFT-over-JMS/MQTT bridge, SOAP services for Symantec Norton Store.

## Writing & Open Source

- **GitHub:** [github.com/rverma-dev](https://github.com/rverma-dev)
- **Technical writing:** multi-agent systems, observability, platform architecture *(articles in progress)*

## Education

<div class="role education">
  <strong>B.Tech (Hons), Indian Institute of Technology Kharagpur</strong>
  <span>Jul 2007 – May 2011</span>
</div>

## Skills

<div class="skills">
  <div><strong>AI & Agent Systems:</strong> multi-agent orchestration, Claude Code hooks, A2A contracts, governance substrates, RAG, LangChain / LangGraph, vector search, LLM evaluation, compliance gating, OpenAI / Anthropic SDKs.</div>
  <div><strong>Platform & Infra:</strong> AWS, Kubernetes / EKS, Istio, Cilium, Spinnaker, Argo Rollouts, GitHub Actions, Terraform / CDK, Nutanix.</div>
  <div><strong>Data & Streaming:</strong> Kafka, Flink, KSQLDB, ClickHouse, TiDB, ScyllaDB, Cassandra, Redis, Hudi, DynamoDB, Druid, Amazon Managed Prometheus.</div>
  <div><strong>Observability & SRE:</strong> OpenTelemetry, Grafana, Prometheus, K6, OpenSearch, custom SIEM, blue-green and canary rollouts.</div>
  <div><strong>Security & Compliance:</strong> zero trust, PCI-DSS, SOC 2, ISO 27001, NPCI / UPI SAR, Keycloak, IAM design.</div>
  <div><strong>Languages:</strong> Go, Python, TypeScript, Java.</div>
</div>
