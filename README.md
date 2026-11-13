# Kloud Kart 12-Month Data Strategy & Architecture

> **Engagement:** AmaliTech Data Engineering Foundations (DE01) Capstone Lab  
> **Client:** Nana Adjei, Head of Operations, Kloud Kart (Accra, Ghana)  
> **Author:** Lead Data Engineering Consultant / Strategist (Samuel Quaigraine)  
> **Repository Status:** Complete, Fully Aligned to Brief & Evalu8 Rubric  

---

## 1. Executive Summary: The Problem in Plain English

Kloud Kart is a three-year-old online retail business based in Accra, Ghana, processing approximately **4,000 customer orders per day** with an active **40 GB MySQL database** and an ongoing expansion pilot in Nigeria. 

The entire platform currently runs on a **single shared physical server** hosting both the customer-facing PHP storefront and the production database, supported by **one sole developer**. This setup creates three acute business failures:
1. **Monday Morning Site Slowdowns:** Heavy analytical reports run directly against the live database, locking tables and slowing the checkout flow for shoppers during peak morning hours.
2. **Conflicting Revenue Numbers:** Operations and Finance rely on private spreadsheets with unaligned formulas, producing persistent weekly revenue discrepancies that stall executive decision-making.
3. **Uncontrolled Customer Data Sprawl:** Raw customer personal details circulate in manual CSV exports across laptops and email chains, creating severe compliance risk (as I understand Act 843) while facing an active 90-day Data Protection Commission (DPC) statutory response deadline.

### The Strategic Solution in Brief
We solve this without unbudgeted cloud infrastructure by activating the pre-approved duplicate server as a dedicated **read replica mirror** (ADR-001) and building a clean, relational reporting schema on Server 2 (ADR-002). We apply **upfront PII sanitization** at the ingest gate while modeling data with SQL (ADR-004), keep live warehouse stock lookups on production while refreshing all analytical reporting via **nightly batch** (ADR-003), and sequence our approved headcount by hiring a **Data Engineer first** (Month 1) and an **Analytics Engineer second** (Month 7) (ADR-005).

---

## 2. Repository Map: Deliverables & Evalu8 Rubric Index

The table below links every file in this repository to the official Evalu8 rubric criteria:

| Deliverable & File | Core Purpose & Scope | Rubric Criterion |
| :--- | :--- | :--- |
| [situation_diagnosis.md](situation_diagnosis.md) | Disentangles symptoms from root causes, models financial impact across sales, labor, and privacy risk, provides stakeholder discovery questions, and explicitly states all operational assumptions. | **Analyze (25%)** |
| [recommendation.md](recommendation.md) | Two-page executive architecture sized for 40 GB, utilizing the pre-approved duplicate server, outlining 90-day staffing milestones, and defending against hard investor questions. | **Evaluate (25%)** |
| [roadmap.md](roadmap.md) | One-page quarterly execution roadmap defining 8 business outcomes written in plain English, each 100% verifiable by Nana Adjei without technical assistance. | **Create (25%)** |
| [decisions/](decisions/) (5 ADRs) | Formal architectural decision records using the required house template: evaluating trade-offs, pricing the cost of error, setting revisit triggers, and defining stress-test survival.<br>- [ADR-001](decisions/ADR-001-reporting-reads-from-read-replica.md): Workload isolation via read replica.<br>- [ADR-002](decisions/ADR-002-relational-warehouse-over-lakehouse.md): Relational MySQL reporting schema over cloud lakehouses.<br>- [ADR-003](decisions/ADR-003-daily-batch-with-oltp-stock-exception.md): Nightly batch ingestion with live stock exception.<br>- [ADR-004](decisions/ADR-004-hybrid-elt-with-pii-masking-under-act-843.md): Upfront PII masking at the gate under Act 843.<br>- [ADR-005](decisions/ADR-005-hiring-data-engineer-then-analytics-engineer.md): Sequencing Data Engineer before Analytics Engineer. | **Evaluate / Create (25%)** |
| [presentation/board_presentation.md](presentation/board_presentation.md) | 10-slide executive board deck accompanied by full, non-technical speaker notes for Nana Adjei, translating technical choices into board-level business decisions. | **Evaluate / Create (25%)** |
| [improvement.md](improvement.md) & [customer_data_inventory_and_deletion_register.md](customer_data_inventory_and_deletion_register.md) | Tangible operational artifact constructed beyond the brief: inventories 5 data sprawl locations, establishes a 90-day DPC statutory deletion register, and creates a Monday revenue reconciliation sign-off protocol. | **Create (25%)** |
| [erd_and_architecture.md](erd_and_architecture.md) | Technical blueprint containing GitHub-safe Mermaid diagrams for high-level system architecture, data pipeline flow, and dimensional reporting entity relationships. | Supporting Architecture |

---

## 3. Hard Engagement Constraints: The Boundary Conditions

Every architectural choice in this repository strictly respects the non-negotiable boundary conditions defined in the brief:

- **Two Data Hires This Financial Year:** Headcount is capped at two roles (no unbudgeted third hire or external agencies).
- **Single Shared Server Must Stay Up:** The live storefront and transactional MySQL database currently share one box; customer checkouts must never be taken offline for reporting tasks.
- **Pre-Approved Second Server:** An identical second hardware box is pre-authorized, providing the exact foundation needed for workload isolation as a read replica without new hosting costs.
- **Act 843 Statutory Deletion Deadline:** Customer data handling must be defensible (as I understand Act 843), with full capability to prove data erasure within the active 90-day Data Protection Commission window.
- **Stock Counts Stay Live:** Warehouse inventory availability must remain accessible in real time to prevent overselling, while all other business reports refresh once daily.
- **Non-Technical Sponsor:** Nana Adjei is non-technical and unavailable for follow-up questions; all deliverables are written in clear business language with all decisions explicitly justified.

---

## 4. Key Operating Assumptions: Where the Brief Was Silent

Because Nana Adjei was unavailable for follow-up interviews, this strategy relies on four explicit, transparent operational assumptions (detailed fully in Section 6 of [situation_diagnosis.md](situation_diagnosis.md)):

1. **Revenue Formula Baseline:** We assume Finance reports net paid orders (cleared payments excluding refunds) while Operations reports gross placed orders. Both formulas are preserved during Q1 and standardized into a single automated SQL definition in Q2.
2. **Financial Costing Baselines:** Lost sales, labor waste, and regulatory risk figures cited in `situation_diagnosis.md` represent analytical baselines (modeled on estimated checkout cart abandonment and executive salaries) rather than audited company ledgers.
3. **Nigeria Expansion Tenancy:** We assume the Nigeria expansion pilot data currently resides within the primary Accra database, partitioned by country code attributes until transaction volume warrants independent local hosting.
4. **Server Hardware Parity:** We assume the pre-approved second server possesses matching CPU, memory, and storage specifications to the primary production server.

---

## 5. How to Navigate This Submission

To evaluate this strategy effectively, follow this recommended three-step reading path:

1. **Start with the Diagnosis:** Read [situation_diagnosis.md](situation_diagnosis.md) to examine the underlying mechanisms, costed problem areas, and explicit operating assumptions.
2. **Review Strategy & Outcomes:** Read [recommendation.md](recommendation.md) for the two-page architecture and investor defense, followed by [roadmap.md](roadmap.md) to inspect the quarterly business outcomes.
3. **Inspect the Technical Depth & Built Artifact:** Examine [decisions/](decisions/) for formal trade-off analyses, [customer_data_inventory_and_deletion_register.md](customer_data_inventory_and_deletion_register.md) for the operational privacy tool, and [presentation/board_presentation.md](presentation/board_presentation.md) for the board deck.

*Note: In accordance with professional data governance standards, no live database credentials, production datasets, or proprietary customer personal records are stored in this repository (configuration templates are provided in [.env.example](.env.example)).*
