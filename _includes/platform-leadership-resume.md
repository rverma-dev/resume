<header class="masthead" style="display: grid; grid-template-columns: 220px 180px 1fr; grid-template-areas: 'identity email linkedin' 'identity phone github'; align-items: center; column-gap: 18px; row-gap: 1px; margin: 0 0 6px 0; font-family: -apple-system, Helvetica, Arial, sans-serif;">
  <div class="identity" style="grid-area: identity;">
    <h1 class="name" style="margin: 0; font-size: 20pt; line-height: 1; letter-spacing: .01em;">Rohit Verma</h1>
    <span class="location" style="display: block; color: #555; font-size: 9.2pt; line-height: 1.25;">Bengaluru, India</span>
  </div>
  <a class="contact-item email" style="grid-area: email; color: #0b4f8a; font-size: 9.2pt; line-height: 1.25; white-space: nowrap; text-decoration: none;" href="mailto:rohitatiit@gmail.com">rohitatiit@gmail.com</a>
  <a class="contact-item phone" style="grid-area: phone; color: #0b4f8a; font-size: 9.2pt; line-height: 1.25; white-space: nowrap; text-decoration: none;" href="tel:+919988844215">+91 99888 44215</a>
  <a class="contact-item linkedin" style="grid-area: linkedin; color: #0b4f8a; font-size: 9.2pt; line-height: 1.25; white-space: nowrap; text-decoration: none;" href="https://www.linkedin.com/in/rohit-verma-24084718">linkedin.com/in/rohit-verma-24084718</a>
  <a class="contact-item github" style="grid-area: github; color: #0b4f8a; font-size: 9.2pt; line-height: 1.25; white-space: nowrap; text-decoration: none;" href="https://github.com/rverma-dev">github.com/rverma-dev</a>
</header>

<div class="profile">
  <p class="intro">Technical platform leader who builds critical infrastructure and scales the teams and operating systems around it.
  Built and operated 0→1 systems at scale including <strong>$240M/month payments infrastructure</strong>, <strong>~80% observability cost-to-serve reduction</strong>, and enterprise-grade SaaS systems on Salesforce Hyperforce.</p>
</div>

## Experience

<div class="role">
  <strong>Principal Engineer (PMTS), MuleSoft (Salesforce)</strong>
  <span>Bengaluru, India; remote US org | Feb 2025 – Present</span>
</div>

Founding technical lead (0→1) for multi-tenant observability, agent federation, and agentic developer systems on Salesforce Hyperforce. For 9 of the first 15 months, provided de-facto execution leadership for the platform program: sprint planning, work grooming, technical direction, operating rhythm, and feedback/promotion calibration input across a 15-engineer US/India team.

<p class="project"><em>Anypoint Monitoring Alerts — Hyperforce re-platform + intelligent alerting</em></p>

- Migrated **3M alerts** off legacy InfluxDB onto Amazon Managed Prometheus in phased rollout; delivered **~80% cost-to-serve reduction** with zero customer-visible SLO regression.
- Multi-tenant alert evaluation platform handling **50K–100K concurrent evaluations** at **P99 < 1s** across ≥2 regions with blue-green deploys.
- Scaled to **60+ AMP workspaces** and **45K alerts per workspace** across enterprise tenants.
- Drove AU/UK/GIA2H rollout work across app + infra repos: new-FI region automation, LaunchDarkly Relay Proxy, GIA-mode wiring, and production deploy config.
- Built AI-native test discipline with `TEST_SCENARIOS` manifests, APIM local firing harnesses, Bruno coverage, and a coherence-validator agent across RFCs/tests/code.
- Designed core platform primitives: tenant sharding, rule sync, buffering, distributed scheduling, and APIM alert migration paths.
- Published a 15-RFC architecture program shaping observability, diagnostics, AI operations, rollout strategy, and multi-tenant platform standards across adjacent teams.

<p class="project"><em>Anypoint Visualizer — Hyperforce re-platform + Druid-native topology</em></p>

- Scales to **10,000+ concurrent orgs**, **~15M applications**, and **~50M edges**, ingesting **500K–1M events/min** at peak.
- **< 5-minute topology freshness SLO** via watermark-based incremental graph construction over Druid.
- Simplified architecture: replaced Logstash with Druid-native ingestion; consolidated `visualizer-janitor` into `visualizer-topology-processor` via k8s leader election.

<p class="project"><em>Proactive Diagnostics / MuleSoft Pulse — AM Agent Federation</em></p>

- Defined architecture for governed AI-assisted operations: agent federation, broker/quarantine/sandbox execution, workflow execution, memory boundaries, security, and platform governance.
- Designed a diagnostic evidence plane that turns alert events into cited AI diagnoses over app logs, metrics, traces, and KB/RAG without exposing raw archives, full logs, heap dumps, or tenant content to prompts.
- Converted passive alerting into a proactive-diagnosis product architecture for **160K alerts/week**, with alert-storm dedup, per-tenant budgets, 5% runtime-overhead cap, source references, degradation flags, and audit/cost controls.

<p class="project"><em>Internal IDE, <a href="https://git.soma.salesforce.com/pages/verma-r/unleash/">Unleash</a></em></p>

- Built an internal Cursor-class IDE for agent-assisted engineering: repo, ticket, PR, terminal, browser, automation, and agent context in one local-first workspace.
- Architected a **four-plane multi-agent decision system** (Knowledge / Decision Graph / Tiered Memory / Governance) with **11 typed agents**, A2A AgentCards, run ledger, path-tiered write authority, compliance hooks, repair detection, and outcomes review.
- Built **Unleash**, a local-first AI engineering IDE from a Superset fork: isolated git worktrees, terminal/chat/file/diff/browser/PR/GUS context, autonomous and coordinator workspaces, automations, and structured A2UI reports.
- Created the Unleash distribution surface with product docs, stable/canary `electron-updater` feeds, DMG release assets, branch-backed GitHub Enterprise Pages publishing, and unauthenticated download verification.

<div class="role">
  <strong>Technology Advisor</strong>
  <span>Bengaluru, India | Mar 2024 – Feb 2025</span>
</div>

- Brandshark: low-latency GenAI video pipeline — chapterization, semantic search, content repurposing.
- DRDO Radar Unit: flight-simulation system with synthetic data generation and MIL/video data integration.
- Gaian Solutions: platform redesign — scaled **20K → 100K QPS**; rebuilt RBAC/ABAC reducing permission checks from **25 s → < 5 ms** at 100K QPS; introduced tenant-context sidecar architecture and cloud FinOps practices.

<div class="role">
  <strong>Vice President / GSL — PaaS, Brane Enterprise</strong>
  <span>Bengaluru, India | Jan 2021 – Jul 2023</span>
</div>

- Architected and delivered the full enterprise SaaS platform — control plane, tenancy, metering, telemetry, billing, on-prem distribution — a MuleSoft-class integration platform for enterprise customers.
- Scaled a 2-engineer platform core into a 40-person platform / DevOps / SRE / security organization; directly built the infrastructure, platform, and security stack that reached enterprise-scale deployment and compliance readiness.
- NSL SaaS Accelerator with just-in-time IaC, reused across Entity Store, Tag Manager, Event Manager, and Schedulers.
- Sidecar event-billing at **10M events/min** with per-tenant rate limiting; workflow engine tuned to **10M TPS** across Kafka, DynamoDB, TiDB, and Redis.
- Full on-prem distribution on Nutanix, ScyllaDB, Kafka, TiDB, and ClickHouse; entity data pipeline on ClickHouse, Redis, Kafka Connect, Glue, and S3.
- Led the 30-person DevOps + SRE operating group across CI/CD (Flux), observability (GLTM), IaC, cost, incident response (Opsgenie + PagerDuty), security.
- Global search on vector embeddings + Elasticsearch (semantic, faceted, typeahead, fuzzy).

<div class="role">
  <strong>Director of Engineering, Jupiter Money</strong>
  <span>Bengaluru, India | Nov 2019 – Jan 2021</span>
</div>

- Single technical owner for ISO 27001, SOC 2, PCI-DSS, NPCI, UPI SAR compliance and partner-bank audits — all passed.
- Hub-and-spoke architecture with partner banks securing all card + UPI transactions at **$240M/month**.
- In-house **SIEM processing 200 GB/hour** on OpenSearch with anomaly detection on banking logs.
- Multi-tenant cloud-data platform on AWS + EMR + Airflow + Flink + Kubernetes.

<div class="role">
  <strong>Director of Engineering, Niki.ai</strong>
  <span>Bengaluru, India | Dec 2017 – Nov 2019</span>
</div>

- Led 3 EMs + 40 engineers; Payment SDK handling **1.2M transactions/day** for B2B partners.
- Dynamo-streams-based order fulfillment on CQRS + event sourcing.
- Replaced manual promotion engine with self-serve Kie rules engine; PCI-DSS multi-account cloud infrastructure.

<div class="role">
  <strong>Senior Software Engineer, Atlassian</strong>
  <span>Bengaluru, India | Aug 2023 – Mar 2024</span>
</div>

- Led JIRA data-migration integration frameworks for external sources across a 9-member engineering team and multiple cross-functional stakeholders.
- Shipped an ALT-text generator for Confluence images using LAVIS (InstructBLIP variant).

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

- Sr. Software Engineer, QA Source (Bebo Technologies): refactored e-commerce platform for multi-tenancy; SOA + ES analytics.
- Software Engineer, Mphasis (HP): core-banking APIs, SWIFT-over-JMS/MQTT bridge, SOAP services for Symantec Norton Store.

## Education

<div class="role education">
  <strong>B.Tech (Hons), Indian Institute of Technology Kharagpur</strong>
  <span>Jul 2007 – May 2011</span>
</div>

## Skills

<div class="skills">
  <div><strong>AI & Agent Systems:</strong> multi-agent orchestration, MCP / A2A contracts, LangGraph, Spring AI, governance substrates, RAG, vector search, LLM evaluation, compliance gating, OpenAI / Anthropic SDKs.</div>
  <div><strong>Platform & Infra:</strong> AWS, Kubernetes / EKS, Istio, Cilium, Spinnaker, Argo Rollouts, GitHub Actions, Terraform / CDK, Nutanix.</div>
  <div><strong>Data & Streaming:</strong> Kafka, Flink, KSQLDB, ClickHouse, TiDB, ScyllaDB, Cassandra, Redis, Hudi, DynamoDB, Druid, Amazon Managed Prometheus.</div>
  <div><strong>Observability & SRE:</strong> OpenTelemetry, Grafana, Prometheus / PromQL, K6, OpenSearch, custom SIEM, anomaly detection, blue-green and canary rollouts.</div>
  <div><strong>Security & Compliance:</strong> zero trust, PCI-DSS, SOC 2, ISO 27001, NPCI / UPI SAR, Keycloak, IAM design.</div>
  <div><strong>Languages:</strong> Go, Python, TypeScript, Java.</div>
  <div><strong>Articles:</strong> multi-agent systems, observability, platform architecture.</div>
</div>
