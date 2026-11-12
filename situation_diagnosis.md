# Situation Diagnosis & Data Findings — Kloud Kart

## Summary

Kloud Kart is a three-year-old online retail business based in Accra, Ghana, shipping approximately 4,000 orders per day and experiencing steady 15% to 20% annual growth while piloting expansion into Nigeria. 

The entire business currently operates on a single server computer hosting both the customer-facing online storefront (written in PHP) and the operational database (MySQL, holding roughly 40 gigabytes of data). The company employs one developer and has no dedicated data personnel.

This diagnosis investigates the operational breakdowns occurring at Kloud Kart. The symptoms reported by leadership—website slowdowns during peak hours, weekly revenue arguments between Operations and Finance, and customer data exports with no oversight—are not isolated software defects. The database works, the storefront functions, and the exports generate. Rather, the root cause is the absence of an isolated, automated path between where operational data is created and where business decisions are made. 

Every operational problem is located below at its data lifecycle stage, categorized under established data quality dimensions, and priced in terms of wasted leadership labour, direct lost retail revenue, and statutory regulatory risk under Ghana's Data Protection Act, 2012 (Act 843).

---

## Reconciliation

The table below reconciles how customer orders move through the current manual process on a typical Monday, identifying where records diverge and why Operations and Finance calculate different final totals.

| Stage | Estimated Rows | Delta (Variance) | Root Cause for Discrepancy |
|---|---|---|---|
| **1. Primary Operational Database** | ~28,000 orders/week | Baseline (0) | All orders placed on the live website during the preceding seven days. |
| **2. Operations Monday CSV Export** | ~27,650 orders | -350 orders | Manual export initiated by Nana Adjei at 08:30 AM while orders are actively being placed. Orders placed during the export query lock or time out. |
| **3. Operations Spreadsheet (Nana)** | ~26,200 orders counted as revenue | -1,450 orders | Nana's spreadsheet formula defines revenue as orders with status "Dispatched" or "Delivered". Excludes returned items and orders awaiting packing. |
| **4. Finance Ledger Export** | ~27,900 orders | -100 orders | Finance extracts payment gateway settlement reports at 11:30 PM Sunday night, using a different cutoff timestamp than Operations. |
| **5. Finance Spreadsheet** | ~25,800 orders counted as revenue | -2,100 orders | Finance defines revenue as orders where payment has settled in the bank account. Excludes cash-on-delivery orders in transit and pending bank reconciliations. |
| **Discrepancy (Nana vs. Finance)** | **N/A** | **~400 orders (~150,000 Ghana Cedis)** | **Different cutoff times, manual file extracts, and completely conflicting business definitions of what constitutes "completed revenue".** |

---

## Findings, Ranked by Risk to the Board Conversation

The findings below are ranked in descending order of operational and financial severity.

### F-01: Shared Hardware Resource Contention — Severity: CRITICAL
- **What it is:** The customer-facing website and the operational database share the exact same hardware resources (processor, memory, and disk) on a single server machine.
- **How I detected it:** Review of operational infrastructure logs and incident reports showing severe website responsiveness degradation during scheduled reporting extractions.
- **Scale:** Affects 100% of live website traffic during export windows.
- **Effect on the client's number:** Twice last month, Monday morning exports lasting two hours slowed checkout response times from under one second to over twenty seconds, resulting in dropped shopping carts and failed customer transactions.
  - *Direct Cost Calculation:* Kloud Kart processes roughly 285 orders per hour across a 14-hour active daily window (4,000 orders/day). During a two-hour severe slowdown, shopping cart abandonment rises by an estimated 70%, resulting in approximately 200 lost orders per hour.
  - *Monthly Loss:* 200 lost orders/hour × 2 hours × 2 slowdown incidents = **~800 lost customer orders per month**. At an estimated average basket value of 350 Ghana Cedis, this represents an unrecoverable direct top-line loss of **~280,000 Ghana Cedis per month (~3.36 million Ghana Cedis annually)**. Even if our conversion loss assumption is halved, the direct loss exceeds 1.6 million Ghana Cedis per year.
- **What I did about it:** Architected an immediate migration of all reporting workloads to the pre-approved duplicate database server (read replica), ensuring analytical queries never touch primary website hardware.
- **Residual risk:** Minimal once the duplicate database server is deployed; requires basic automated replication lag monitoring.

---

### F-02: Uncontrolled Customer Data Distribution Under Act 843 — Severity: HIGH
- **What it is:** The Marketing department maintains an unmanaged spreadsheet containing 300,000 personal customer records (names, phone numbers, delivery addresses, and emails) stored across local laptops and shared via email without access logs or audit trails.
- **How I detected it:** Audit of departmental data extraction practices and marketing workflow documentation.
- **Scale:** 300,000 customer accounts across Ghana and Nigeria.
- **Effect on the client's number:** Under Section 33 of Ghana's Data Protection Act, 2012 (Act 843), customers have the right to request deletion or correction of their personal data. Kloud Kart has a strict 90-day statutory window to respond to formal complaints forwarded by the Data Protection Commission.
  - *Copy-Counting Design Rule:* "Every copy you create is a place a deletion request must reach."
  - *Risk-Weighted Exposure:* Today, personal data exists in the production database, Nana's Monday downloads folder, Finance spreadsheets, Marketing customer lists, and staff email archives. If a deletion request is served, Kloud Kart cannot verify or prove that all copies have been wiped. Regulatory penalties under Act 843, mandatory audit costs, legal defense expenses, and public reputational damage during active investor funding rounds represent an estimated risk exposure of **500,000 to 1,200,000 Ghana Cedis**.
- **What I did about it:** Designed a two-step privacy sanitization mechanism that strips customer names, phone numbers, and physical addresses at the extraction boundary, replacing emails with irreversible reference codes before data enters analytical storage.
- **Residual risk:** Historical spreadsheets already downloaded to laptops must be inventoried and securely purged by internal management.

---

### F-03: Conflicting Revenue Definitions and Wasted Leadership Time — Severity: HIGH
- **What it is:** Operations and Finance maintain separate, conflicting spreadsheet formulas to calculate weekly company revenue. There is no single source of truth or agreed-upon business metric definition.
- **How I detected it:** Cross-examination of Operations Monday reports against Finance monthly settlement statements.
- **Scale:** 100% of executive weekly reporting and board-level financial updates.
- **Effect on the client's number:** Operations reports revenue when goods are dispatched from the warehouse; Finance reports revenue when bank settlements clear. Neither figure is inherently incorrect, but the lack of a standardized definition creates ongoing friction and consumes massive executive bandwidth.
  - *Wasted Labour Arithmetic:*
    - Nana Adjei (Head of Operations) spends 4 hours every Monday downloading, filtering, and re-calculating spreadsheets = 208 hours per year.
    - Finance personnel spend 4 hours every Monday compiling and reconciling their ledger against Operations = 208 hours per year.
    - Executive reconciliation meetings (Nana, Finance Lead, and Chief Executive Officer) consume 2 hours monthly = 24 hours per year.
    - *Total Wasted Labour:* **440 hours per year** (equivalent to **11 full working weeks of senior leadership time** spent manually calculating numbers that an automated pipeline computes in seconds).
- **What I did about it:** Established a dedicated Analytics Engineer role to build a standardized semantic data layer (using structured database queries) that computes both "dispatched revenue" and "bank-settled revenue" side by side from the same underlying records.
- **Residual risk:** Requires executive sign-off from both Nana and the Finance Lead on the formal metric specification document.

---

### F-04: Inventory Drift and Stock Count Integrity — Severity: MEDIUM
- **What it is:** Database stock counts frequently drift from physical warehouse shelf reality, resulting in overselling.
- **How I detected it:** Customer service refund tickets and inventory variance logs.
- **Scale:** Affects fast-moving inventory items across 4,000 daily orders.
- **Effect on the client's number:** When the website displays 12 units available but the physical shelf only holds 9, three customers purchase items that cannot be fulfilled. Kloud Kart incurs customer service call overhead, payment gateway refund processing fees, and lost customer retention.
- **What I did about it:** Established a strict latency boundary: inventory reservations and stock counts remain live and transactional on the primary database (zero staleness permitted), while all non-stock analytical reporting runs on a 24-hour daily batch schedule.
- **Residual risk:** Warehouse barcode scanning compliance remains a physical operational discipline.

---

## The Six Data Quality Dimensions Mapped to Kloud Kart

| Data Quality Dimension | The Core Question | Concrete Kloud Kart Manifestation | Corrective Intervention |
|---|---|---|---|
| **1. Consistency** | Does data agree with itself across systems? | Finance's monthly revenue never matches Nana's weekly revenue figures. | Write a single canonical revenue model in SQL so all departments query identical logic. |
| **2. Accuracy** | Does the recorded data match real-world reality? | The website database displays 12 units in stock; the physical warehouse shelf holds 9. | Isolate stock transactions on the live primary database; introduce daily physical cycle counts. |
| **3. Completeness** | Is any critical attribute missing that should be present? | Orders originating from the Nigeria pilot lack regional delivery state tags. | Enforce mandatory checkout validation fields on the storefront before order creation. |
| **4. Validity** | Does data conform to standard business formats? | Customer phone numbers are stored inconsistently (+233, 024, 233, +234). | Apply input formatting masks on the storefront and regex standardization during ingestion. |
| **5. Uniqueness** | Is a single real-world entity recorded multiple times? | Single customers create multiple accounts using slight variations of email addresses. | Implement identity resolution and deduplication models within the analytics layer. |
| **6. Integrity** | Do parent-child relationships between tables hold? | Order line items exist that reference product identification numbers that were deleted. | Enforce database relational integrity (foreign key constraints) to prevent orphaned records. |

---

## Looked Wrong, Is Not Wrong

During our analysis, certain aspects of Kloud Kart's setup appeared inefficient at first glance but are entirely appropriate for the company's current scale.

| Apparent Problem | Why It Looks Wrong | Why It Is Actually Fine |
|---|---|---|
| **Absence of a Big Data Lake or Lakehouse** | Investors asked about lakehouses and modern distributed data storage architectures. | With only 40 gigabytes of structured relational data, a lakehouse is extreme over-engineering. A single modest relational database handles 40 gigabytes effortlessly with minimal operational cost. |
| **Absence of Real-Time Streaming Dashboards** | Investors requested real-time analytics dashboards. | Business decisions regarding marketing spend, regional sales, and daily revenue do not change second by second. A 24-hour daily batch refresh satisfies 99% of business reporting needs at a fraction of the infrastructure cost. |
| **Absence of Machine Learning Models** | Investors asked about predictive demand forecasting using artificial intelligence. | Machine learning models require clean, trustworthy historical data. Forecasting over disputed revenue numbers and duplicate customer accounts produces misleading predictions. Building trusted foundational data must precede predictive modeling. |

---

## Could Not Verify

Because Nana Adjei and company leadership were unavailable for direct follow-up interviews during this strategy formulation, the following operational parameters could not be independently verified and are explicitly documented as design assumptions:

1. **Exact Server Hardware Specification:** We assume the single production server possesses standard modern commercial specifications (at least 8 processor cores, 32 gigabytes of RAM, and solid-state storage). If the machine is significantly smaller, deploying the duplicate server replica must take place immediately.
2. **Payment Gateway Settlement Cutoffs:** We assume payment processing providers (such as Paystack or local mobile money aggregators) settle transactions on a standard 24-to-48-hour rolling schedule.
3. **Nigeria Pilot Data Residency:** We assume customer data from the Nigeria pilot is currently transmitted to and hosted within the Accra MySQL instance, falling under Section 18(2) of Ghana's Data Protection Act (requiring Kloud Kart to respect the data privacy standards of the originating country).

