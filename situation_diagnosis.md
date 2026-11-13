# Situation Diagnosis: Root Causes, Costed and Ranked by Risk: Kloud Kart

## 1. Executive Summary

Kloud Kart is an e-commerce company in Accra, Ghana, operating for three years. The company ships about 4,000 orders a day, grows 15% to 20% a year, and is currently piloting an expansion in Nigeria.

The company's entire technical footprint sits on a single physical server machine. This single machine runs both the public customer storefront (built in PHP) and the operational database (running MySQL with roughly 40 gigabytes of data). Kloud Kart employs one software developer and has no dedicated data staff.

This diagnosis investigates the operational breakdowns reported by company leadership:

- **Nana Adjei**, Head of Operations
- The **Finance Department**
- The **Board of Directors**

The symptoms they observe every week, such as website slowdowns during peak shopping hours, arguments over weekly revenue totals, and uncontrolled customer spreadsheets circulating on laptops, are not software bugs. The website functions, the database writes orders, and the spreadsheets export.

The true underlying root cause is structural: **Kloud Kart has no separate, automated path between where live sales happen and where business reports are created.**

Below, we separate the visible symptoms from their root causes, explain the technical mechanisms in plain language, price each problem in terms of real money, rank them by risk to the board, and list the discovery questions we would have asked Nana Adjei had she been available for interview.

---

## 2. Separating Root Causes from Visible Symptoms

| Observed Symptom                                                                                                                                                                                                                                                                        | Why It Looks Like the Problem                                                                                                                     | The True Root Cause (Underlying Mechanism)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The website freezes or slows down on Monday mornings between 08:00 AM and 10:00 AM.                                                                                                                                                                                                     | Staff assume the web server is overloaded by customer traffic or that the PHP code is poorly written.                                             | **One Machine Doing Two Jobs:** Nana Adjei runs a heavy, two-hour report directly on the live store’s database while customers are shopping. Because both tasks share one machine, the report uses up the power the website needs to run smoothly.                                                                                                                                                                                                                                                                                    |
| Operations (Nana) and Finance report two different weekly revenue totals, and neither team can prove whose number is right, delaying executive decisions.                                                                                                                               | Staff assume one department has a typing error or broken formula in their spreadsheet.                                                            | **No Single Source of Truth or Shared Metric Definition:** Neither department works from a shared, written definition of "revenue" (e.g., whether to count orders on placement, payment, or delivery, or how to treat refunds). Because both teams pull separate CSV exports at different times into isolated spreadsheets, they are calculating different formulas on different snapshots of the data.                                                                                                                               |
| Staff (including Nana in Operations, Finance, and Marketing) manually export customer lists (estimated at ~300,000 records) as CSV files, while Kloud Kart faces an active Data Protection Commission complaint requiring proof within 90 days that a customer’s data has been deleted. | Staff across Operations, Finance, and Marketing treat manual CSV downloads and shared spreadsheets as normal, harmless day-to-day reporting work. | **Untracked File Copies and Open Access:** Because staff across Operations, Finance, and Marketing lack safe, masked self-service reporting views, staff routinely export raw customer lists (including Marketing's ~300,000-person list and Operations/Finance extracts) into uncounted local CSV files and spreadsheets. As I understand Act 843, allowing untracked copies of personal data to sit outside the main database makes it impossible to locate and permanently erase every copy within the 90-day regulatory deadline. |

## 3. Costing the Root Causes: Three Types of Financial Impact

To help the Board of Directors make clear investment decisions, each root cause is priced below across three distinct financial categories: direct lost retail revenue, wasted leadership labour, and legal regulatory risk.

### Root Cause 1: Heavy Manual Exports Slowing Down Customer Checkout

- **Where it occurs in the data lifecycle:** Storage and Querying.
- **Data Quality Dimension affected:** Timeliness and System Availability.
- **The Mechanism:** The live PHP shop and Nana's Monday morning reporting query run on the exact same server hardware. When Nana queries thousands of customer rows across multiple large tables, the database locks table rows and consumes a large amount of available memory and processor capacity.
- **Costing (Illustrative Financial Impact Model):**
  - _Direct Lost Sales:_ Kloud Kart averages 285 orders per hour during its 14-hour daily active window (shipping 4,000 orders per day). During a two-hour severe slowdown, checkout wait times jump from under 1 second to over 20 seconds. Applying standard e-commerce cart-abandonment benchmarks (estimated at a 70% checkout abandonment spike during severe delays, detailed under Operating Assumptions in Section 6), an estimated 200 orders are lost per hour.
  - _Monthly Order Loss:_ 200 lost orders per hour × 2 hours × 2 slowdown incidents per month = **an illustrative loss of approximately 800 customer orders per month**.
  - _Estimated Revenue Impact:_ At an assumed average basket value of 350 Ghana Cedis, this models an illustrative loss of **approximately 280,000 Ghana Cedis per month (3.36 million Ghana Cedis annually)**. Even if conservatively halved, the business models over 1.6 million Ghana Cedis in lost sales every year.
- **What we decided to do:** We planned an immediate move of all reporting tasks to the pre-approved duplicate database server (the reporting mirror). This guarantees that reports and exports run on separate hardware and never touch the live storefront machine.
- **Remaining risk:** Low once the second server is turned on. It only requires a basic check to ensure the mirror stays in sync with the live database.

---

### Root Cause 2: Uncontrolled Customer Data Distribution Under Act 843

- **Where it occurs in the data lifecycle:** Ingestion, Storage, and Consumption.
- **Data Quality Dimension affected:** Validity, Privacy Governance, and Security.
- **The Mechanism:** Staff across Operations, Finance, and Marketing manually export customer data into untracked CSV files and spreadsheets (including Marketing's ~300,000-person customer list and daily operational extracts) containing personal customer records that sit on unmanaged local laptops and shared folders.
- **Costing:**
  - _The Compliance Rule:_ As I understand Act 843, individuals have the right to request the correction or deletion of their personal data, and Kloud Kart faces a strict 90-day deadline to answer the active complaint from the Data Protection Commission.
  - _The Copy-Counting Rule:_ Every copy you create is a place a deletion request must reach.
  - _Risk-Weighted Exposure:_ If a deletion verification check arrives today, Kloud Kart cannot locate or erase records sitting on staff laptops. Potential regulatory sanctions, audit and legal fees, and investor due-diligence friction create an illustrative risk-weighted exposure of **500,000 to 1,200,000 Ghana Cedis**.
- **What we decided to do:** We planned a strict privacy gateway. Before any customer transaction data enters the reporting system, personal names, phone numbers, and physical home addresses are permanently removed at the gate. Customer emails are converted into irreversible anonymous codes (such as turning an email into `cust_98234`).
- **Remaining risk:** Historical spreadsheets already saved on employee laptops must be identified and safely erased by company management.

---

### Root Cause 3: Conflicting Business Logic and Manual Spreadsheets

- **Where it occurs in the data lifecycle:** Transformation and Consumption.
- **Data Quality Dimension affected:** Consistency and Accuracy.
- **The Mechanism:** Operations and Finance have never agreed on a standardized formula for revenue, such as whether to count orders on placement, dispatch, or payment settlement, or how to handle refunds, and both teams pull separate CSV exports at different times into private spreadsheets.
- **Costing (Illustrative Labour Impact Model):**
  - _Wasted Executive Labour:_ Nana Adjei (Head of Operations) and the Finance Lead spend an estimated 4 hours every Monday morning comparing spreadsheets, tracing individual order rows, and debating conflicting numbers before executive meetings.
  - _Annual Labour Waste:_ 4 hours per week × 2 senior department leaders × 52 weeks = **an illustrative 416 executive hours wasted per year** (equivalent to over 10 full working weeks of senior leadership bandwidth).
  - _Estimated Salary Cost:_ At an assumed blended leadership rate of 200 Ghana Cedis per hour (detailed under Operating Assumptions in Section 6), this models approximately **83,200 Ghana Cedis per year** in executive payroll spent acting as manual spreadsheet calculators.
  - _Strategic Cost:_ More importantly, the Managing Director and the Board of Directors cannot trust weekly financial statements, creating cash planning blind spots and delaying executive decisions.
- **What we decided to do:** We planned a single, centralized reporting table where the formula for confirmed revenue is locked into clear, testable database queries (SQL) maintained by the Analytics Engineer. Both departments will read from this single source of truth.
- **Remaining risk:** Moderate until Nana Adjei and the Finance Lead formally sign off on the standard business definitions.

---

## 4. Ranking by Risk to the Board Conversation

When presenting to the Board of Directors, technical issues must be prioritized by business risk rather than technical difficulty or daily irritation:

```
+-----------------------------------------------------------------------------------+
| RANK 1: CRITICAL BUSINESS THREAT (Regulatory Survival)                           |
| Issue: Uncontrolled Customer Data under Ghana's Data Protection Act (Act 843)     |
| Business Impact: 500,000 to 1,200,000 Ghana Cedis in legal exposure and fines.    |
| Action: Strip personal data at the gate; delete unmanaged laptop spreadsheets.     |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| RANK 2: DIRECT REVENUE DESTRUCTION (Immediate Cash Flow)                         |
| Issue: Monday checkout slowdowns caused by shared database hardware               |
| Business Impact: ~280,000 Ghana Cedis per month (~3.36M Cedis/year) in lost sales |
| Action: Move all reports to the pre-approved duplicate database server (mirror).  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| RANK 3: OPERATIONAL PARALYSIS (Governance and Labour Waste)                       |
| Issue: Conflicting weekly revenue definitions between Operations and Finance      |
| Business Impact: >416 wasted executive hours per year; board distrust in metrics  |
| Action: Centralize revenue logic in SQL models; eliminate private spreadsheets.   |
+-----------------------------------------------------------------------------------+
```

---

## 5. Discovery Questions for Nana Adjei

Because Nana Adjei and company leadership were not available for direct follow-up discussions during this strategy engagement, we formulated our recommendations on explicit operating assumptions. Had Nana been available, we would have asked the following targeted questions to refine our findings:

1. **Server Hardware Specifications:**
   - _Question:_ "What are the exact hardware specifications of the current server (processor core count, RAM capacity, and disk storage type), and is the pre-approved second server identical in hardware?"
   - _Why this matters:_ Confirms whether the current machine has enough memory to buffer database indexes and verifies that the mirror server can take over instantly if the primary server fails.

2. **Payment Gateway Settlement Schedules:**
   - _Question:_ "What are the exact settlement cutoff hours and clearing schedules for card payment processors and mobile money providers in Ghana and Nigeria?"
   - _Why this matters:_ Allows the Analytics Engineer to align the daily reporting batch schedule with actual bank deposits, closing the gap between shipped orders and cleared cash.

3. **Customer Return and Refund Timelines:**
   - _Question:_ "What is Kloud Kart's average return window, what percentage of dispatched orders are returned, and at what exact stage does Finance issue a customer refund?"
   - _Why this matters:_ Ensures that returned merchandise is automatically deducted from net revenue models rather than manually adjusted weeks later in spreadsheets.

4. **Nigeria Pilot Data Storage:**
   - _Question:_ "Does the Nigeria expansion pilot store its customer data in the same MySQL database in Accra, or does it use a separate hosting service in Lagos?"
   - _Why this matters:_ Governs cross-border data transfer rules under Section 18 of Ghana's Act 843 and the Nigeria Data Protection Act.

5. **Cross-Departmental Customer Data Downloads:**
   - _Question:_ "What specific customer attributes do teams across Marketing, Operations, and Finance genuinely need for daily reporting, and why are complete spreadsheets of ~300,000 customer records being downloaded to local computers?"
   - _Why this matters:_ Helps us build secure, privacy-compliant aggregated customer reports so staff never need raw personal contact files again.

---

## 6. Operating Assumptions (Where the Brief Is Silent)

Because Nana Adjei is unavailable for follow-up questions, this diagnosis and the accompanying architectural recommendations rely on the following explicit operating assumptions where the brief does not provide primary company data:

1. **Revenue Formula Definition:** The brief states that Nana's Monday spreadsheet never matches Finance's spreadsheet, but does not provide their exact accounting formulas. We assume Finance reports net cleared orders (paid transactions excluding customer refunds) and Operations reports gross placed orders. During Quarter 1, both formulas will be standardized into clear, auditable database queries. If company leadership defines confirmed revenue strictly by bank deposit settlement timestamp, only the filter criteria in our reporting query change.
2. **Financial Costing Baselines (Root Causes 1 and 3):** The brief states that twice last month a Monday export slowed the live site to a crawl, and that weekly revenue numbers conflict, but provides no audited financial ledger, average order value, cart abandonment statistics, or payroll figures. To provide the Board of Directors with a concrete financial scale of impact, we modeled the following baseline parameters:
   - _Lost Sales Model (Root Cause 1):_ Assumes an active 14-hour daily order window (~285 orders/hour from shipping 4,000 daily orders), a 70% shopping cart abandonment spike when checkout response latency jumps from under 1 second to over 20 seconds during two-hour slowdowns (~200 lost orders/hour, or ~800 lost orders across two monthly incidents), and an average basket value of 350 Ghana Cedis (~280,000 Ghana Cedis/month).
   - _Labour Waste Model (Root Cause 3):_ Assumes an average of 4 hours spent each Monday by 2 senior leaders (Nana Adjei and the Finance Lead) reconciling conflicting spreadsheets (416 leadership hours annually), at an assumed blended leadership rate of 200 Ghana Cedis per hour (~83,200 Ghana Cedis annually).
   - _Integrity Note:_ These costing figures represent analytical models rather than company financial records. If verified company ledgers indicate higher or lower basket sizes or salary figures, only the financial multipliers scale; the underlying root causes, operational risks, and architectural solutions remain completely identical.
3. **Nigeria Pilot Data Tenancy:** The brief notes that Kloud Kart is shipping about 4,000 orders per day and piloting in Nigeria, with orders, inventory, and customer accounts living in one MySQL database on the same box as the website. We assume orders from the Nigeria expansion pilot write to this same Accra MySQL database (partitioned by country code attributes) rather than a separate hosted server in Nigeria. If a separate database is deployed in Nigeria later, our ingestion pipeline simply adds a second source connection.
4. **Payment Gateway Settlement Cutoffs:** In the absence of primary payment gateway clearing schedules, we assume third-party card payment processors and mobile money providers operate on standard 24-to-48-hour rolling settlement windows.
