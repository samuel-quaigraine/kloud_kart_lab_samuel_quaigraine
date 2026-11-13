# ADR-005: Hire a Data Engineer First, Then an Analytics Engineer (No Data Scientist)

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decision owner:** Nana Adjei (Head of Operations) and Kloud Kart Leadership (advised by External Data Consultant)

## Context

Kloud Kart's board has approved budget for exactly **two data hires** during this financial year, not three. The current technology team consists of one developer who maintains the PHP website and MySQL database. 

Following the funding round, investors emphasized artificial intelligence and predictive demand forecasting. Nana Adjei must present a staffing plan that addresses immediate site slowdowns, resolves weekly revenue disputes between Operations and Finance, and complies with Ghana's Data Protection Act, 2012 (Act 843), without exceeding the two-person headcount constraint.

## Decision

We sequence the two budgeted hires chronologically by operational risk:
1. **Hire 1 (Month 1): Data Engineer.** Accountable for data infrastructure, database replication, automated nightly pipelines, data sanitization, and protecting the live shop from slowdowns. In their first 30 days, they stop website slowdowns by connecting Server 2; by Day 60, they automate the nightly cleaned data copy; by Day 90, they implement customer deletion safeguards and resolve the DPC complaint.
2. **Hire 2 (Month 3): Analytics Engineer.** Accountable for the business calculation layer, standardized metric definitions in Structured Query Language (SQL), and automated daily reconciliation dashboards. In their first 30 days (Month 4), they deliver the agreed sales formula; by Day 60 (Month 5), they turn on daily sales variance and stock drift alerts; by Day 90 (Month 6), they roll out self-service reports for all departments.

We explicitly decide **not to staff a Data Scientist or Artificial Intelligence Engineer** this year.

## Alternatives considered

### Alternative A: Hire a Data Scientist first (or one Data Scientist and one Data Engineer)

- **How it would work:** The first hire is a Data Scientist tasked with building predictive machine learning models in Python to forecast inventory demand and impress board investors.
- **Why it is attractive:** It directly matches investor interest in artificial intelligence and machine learning.
- **Why rejected:** Prediction sits on top of trustworthy history. If Monday's revenue number is disputed between Operations and Finance, and inventory records drift from physical warehouse reality, any machine learning forecast built on top of that data will produce inaccurate forecasts with mathematical confidence. A Data Scientist does not have the systems engineering skills to stop website slowdowns, configure database replication, or secure data pipelines under Act 843. Hiring a Data Scientist before basic data reliability exists is an expensive failure mode.

### Alternative B: Hire two general software developers

- **How it would work:** Recruit two mid-level software developers with general PHP and SQL experience to handle both web features and data reporting tasks.
- **Why it is attractive:** Provides flexible engineering capacity across the general technology backlog.
- **Why rejected:** Kloud Kart already has one general developer (PHP and MySQL), and the current operational crisis occurred under that model. General developers typically lack specialized training in data lifecycle architecture, data privacy regulations (Act 843 compliance), and semantic metric modeling. Without dedicated accountability, data infrastructure remains an unowned side task.

## Consequences

- **What this buys:** Immediate operational relief. The Data Engineer stops the live website slowdowns within their first 30 days. The Analytics Engineer eliminates executive revenue disputes by Month 4. The division of accountability is unmistakable: the Data Engineer is called if data fails to arrive or arrives late; the Analytics Engineer is called if two departments define a number differently.
- **What this costs:** Kloud Kart builds no custom predictive machine learning algorithms in year one. Predictive demand forecasting is deferred to year two.
- **What it costs the client if I am wrong:** If an investor threatens to withhold growth capital unless an artificial intelligence algorithm is deployed immediately, Nana will have to defend why establishing trusted foundational data was prioritized over an early machine learning prototype.
- **What would make me revisit this:** Foundational pipelines and revenue reconciliation stabilizing significantly ahead of schedule, paired with severe warehouse holding costs that create an undeniable business case for predictive forecasting in the fourth quarter.

## What this survives

This hiring strategy comfortably survives Kloud Kart's current operational scale, keeps payroll strictly within the board's approved two-person budget, and builds an enduring foundation that can support machine learning in future years.
