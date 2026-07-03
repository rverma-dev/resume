---
layout: default
title: Rohit Verma — Platform Engineering
---

<nav class="site-nav" aria-label="Primary navigation">
  <a class="site-logo" href="{{ '/' | relative_url }}">Rohit Verma</a>
  <div class="site-nav-links">
    <a href="#resumes">Resumes</a>
    <a href="{{ '/jobs/' | relative_url }}">Applications</a>
    <a href="#connections">Connections</a>
    <a href="#work">Work</a>
  </div>
  <a class="site-nav-action" href="{{ '/resume/' | relative_url }}">Open Resume</a>
</nav>

<main class="site-shell">
  <section class="site-hero" id="top">
    <div class="site-hero-content">
      <p class="site-kicker">Technical Director / Head of Platform Engineering</p>
      <h1>Building platform systems, then scaling the teams that operate them.</h1>
      <p class="site-hero-copy">
        Fifteen years across observability, cloud infrastructure, fintech,
        enterprise SaaS, and AI engineering. I combine deep architecture with
        operating systems for teams: roadmap shaping, execution rhythm,
        automation, reliability, and product intuition.
      </p>
      <div class="site-hero-actions">
        <a class="site-button primary" href="{{ '/resume/' | relative_url }}">Resume</a>
        <a class="site-button" href="{{ '/jobs/' | relative_url }}">Applications Tracker</a>
      </div>
    </div>
    <div class="site-proof-strip" aria-label="Career proof points">
      <div><strong>3M</strong><span>alert definitions migrated with no customer-visible SLO regression</span></div>
      <div><strong>80%</strong><span>observability cost-to-serve reduction</span></div>
      <div><strong>40</strong><span>engineers across platform, DevOps, SRE, and security scope</span></div>
      <div><strong>$240M/mo</strong><span>payments infrastructure at Jupiter Money</span></div>
    </div>
  </section>

  <section class="site-section" id="resumes">
    <div class="section-heading">
      <p class="site-kicker">Resume System</p>
      <h2>One profile, targeted surfaces.</h2>
      <p>
        The public site should not hedge. Each resume variant carries one
        coherent story for one role family.
      </p>
    </div>

    <div class="resume-tabs">
      <input type="radio" name="resume-tab" id="tab-platform" checked>
      <input type="radio" name="resume-tab" id="tab-architect">
      <input type="radio" name="resume-tab" id="tab-director">
      <div class="tab-list" role="tablist" aria-label="Resume variants">
        <label for="tab-platform">Head of Platform</label>
        <label for="tab-architect">Principal Architect</label>
        <label for="tab-director">Director Variant</label>
      </div>

      <div class="tab-panels">
        <article class="tab-panel platform-panel">
          <h3>Technical Director / Head of Platform Engineering</h3>
          <p>
            Primary target for build-a-function and modernization roles: lead
            through EMs, keep architecture in hand, and scale execution systems
            around critical platforms.
          </p>
          <a href="{{ '/resume/' | relative_url }}">Open printable resume</a>
        </article>
        <article class="tab-panel architect-panel">
          <h3>Senior Principal / Principal Architect</h3>
          <p>
            Fallback and high-probability path for top IC ladders: 0-&gt;1
            platforms, multi-team technical direction, RFC programs, and the
            hardest distributed systems work in the room.
          </p>
          <a href="{{ '/resume/base_resume.md' | relative_url }}">Open base Markdown</a>
        </article>
        <article class="tab-panel director-panel">
          <h3>Director, Platform Engineering</h3>
          <p>
            Specialized variant for roles that explicitly need a builder who can
            grow a function: Brane 2-&gt;40, Niki 3 EMs / 40 engineers, and
            Salesforce de-facto platform-program leadership.
          </p>
          <a href="{{ '/companies/_samples/director-platform/resume.md' | relative_url }}">Open Director draft</a>
        </article>
      </div>
    </div>
  </section>

  <section class="site-section split-section" id="applications">
    <div class="section-heading">
      <p class="site-kicker">Applications</p>
      <h2>Approval-gated static workflow.</h2>
    </div>
    <div class="site-grid three">
      <article>
        <h3>Discover</h3>
        <p>LinkedIn discovery stays read-only and writes candidates as unreviewed jobs.</p>
      </article>
      <article>
        <h3>Approve</h3>
        <p>Selected jobs route through GitHub Issues so the static site can request changes without a database.</p>
      </article>
      <article>
        <h3>Publish</h3>
        <p>The scheduler polls issue metadata, imports approvals or rejections, and republishes GitHub Pages.</p>
      </article>
    </div>
    <div class="site-actions-row">
      <a class="site-button primary" href="{{ '/jobs/' | relative_url }}">Open tracker</a>
      <a class="site-button" href="https://github.com/rverma-dev/resume/issues/new">Open GitHub issue composer</a>
    </div>
  </section>

  <section class="site-section split-section" id="connections">
    <div class="section-heading">
      <p class="site-kicker">Connections</p>
      <h2>Warm paths matter more than cold applications.</h2>
      <p>
        The best Director jump is usually backchannel-led. This site should make
        connection tracking a first-class workflow alongside job discovery.
      </p>
    </div>
    <div class="site-grid two">
      <article>
        <h3>Target map</h3>
        <p>Prioritize India, UAE, Singapore, UK, EU, and internal Salesforce paths. Treat external US roles as low-probability unless sponsorship is explicit.</p>
      </article>
      <article>
        <h3>Reference path</h3>
        <p>Collect people who can credibly say: he already led the platform program, shaped execution, and can own the org.</p>
      </article>
    </div>
  </section>

  <section class="site-section" id="work">
    <div class="section-heading">
      <p class="site-kicker">Work System</p>
      <h2>The evidence is the differentiator.</h2>
      <p>
        Banking, observability, compliance, agent platforms, developer tooling,
        DRDO simulation, and enterprise integration work should become curated
        evidence surfaces, not private recollection.
      </p>
    </div>
    <div class="site-grid four">
      <article><h3>Platform</h3><p>Hyperforce alerting, Brane PaaS, Jupiter banking infrastructure.</p></article>
      <article><h3>AI Systems</h3><p>Agent federation, local-first IDE, governed diagnostic workflows.</p></article>
      <article><h3>Compliance</h3><p>PCI-DSS, SOC 2, ISO 27001, NPCI, UPI SAR, partner-bank audits.</p></article>
      <article><h3>Product</h3><p>Startup product intuition across fintech, marketplaces, travel, and developer tools.</p></article>
    </div>
  </section>
</main>
