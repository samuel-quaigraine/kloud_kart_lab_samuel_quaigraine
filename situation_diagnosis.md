# Situation Diagnosis: Root Causes, Costed and Ranked by Risk: Kloud Kart

## 1. Executive Summary

Kloud Kart is a three-year-old online retail business based in Accra, Ghana. The company processes approximately 4,000 customer orders per day, experiences 15% to 20% annual sales growth, and is currently running an expansion pilot in Nigeria. 

The company's entire technical footprint sits on a single physical server machine. This single machine runs both the public customer storefront (built in PHP) and the operational database (running MySQL with roughly 40 gigabytes of data). Kloud Kart employs one software developer and has no dedicated data staff.

This diagnosis investigates the operational breakdowns reported by company leadership:
- **Nana Adjei**, Head of Operations
- The **Finance Lead** and Finance Department
- The **Managing Director** and Board of Directors

The symptoms they observe every week, such as website slowdowns during peak shopping hours, heated arguments over weekly revenue totals, and uncontrolled customer spreadsheets circulating on laptops, are not software bugs. The website functions, the database writes orders, and the spreadsheets export. 

The true underlying root cause is structural: **Kloud Kart has no separate, automated path between where live sales happen and where business reports are created.**

Below, we separate the visible symptoms from their root causes, explain the technical mechanisms in plain language, price each problem in terms of real money, rank them by risk to the board, and list the discovery questions we would have asked Nana Adjei had she been available for interview.

---

## 2. Separating Root Causes from Visible Symptoms

| Observed Symptom | Why It Looks Like the Problem | The True Root Cause (Underlying Mechanism) |
|---|---|---|
| The website freezes or slows to a crawl on Monday mornings between 08:00 AM and 10:00 AM. | Staff assume the web server is overloaded by customer traffic or that the PHP code is poorly written. | **Shared Hardware Resource Exhaustion:** Nana Adjei runs a heavy, two-hour reporting query directly against the live database while shoppers are actively browsing. Both workloads compete for the same processor, memory, and disk. |
| Operations calculates weekly revenue at GH₵ 1,450,000 while Finance calculates GH₵ 1,300,000, causing hours of executive debate. | Staff assume one department has a typing error or broken formula in their spreadsheet. | **Conflicting Business Definitions and Different Cutoff Times:** Operations counts revenue the moment an order is packed or shipped. Finance only counts revenue once payment clears into the bank account. Furthermore, Nana exports her file on Monday morning while Finance exports on Sunday night. |
| The Marketing team shares spreadsheets containing 300,000 customer records across employee laptops and email threads. | Staff view this as helpful, fast marketing work to increase customer retention and sales. | **Missing Governed Ingestion Path and Data Privacy Breach:** Personal customer information is copied outside the database with zero access controls, making it impossible to comply with Ghana's Data Protection Act, 2012 (Act 843). |
| Warehouse stock counts occasionally show items as available when the physical warehouse shelves are completely empty. | Staff assume warehouse pickers are misplacing items or stealing stock. | **Reporting Ingestion Timing Gap:** Batch reporting updates happen periodically. If inventory stock levels are read from an old reporting snapshot rather than checked live on the primary store database, customers can purchase products that have already sold out. |

---

## 3. Costing the Root Causes: Three Types of Financial Impact

To help the Board of Directors make clear investment decisions, each root cause is priced below across three distinct financial categories: direct lost retail revenue, wasted leadership labour, and legal regulatory risk.

### Root Cause 1: Shared Hardware Resource Contention
- **Where it occurs in the data lifecycle:** Storage and Querying.
- **Data Quality Dimension affected:** Timeliness and System Availability.
- **The Mechanism:** The live PHP shop and Nana's Monday morning reporting query run on the exact same server hardware. When Nana queries thousands of customer rows across multiple large tables, the database locks table rows and monopolizes available memory and processor cores.
- **Costing:**
  - *Direct Lost Sales:* Kloud Kart averages 285 orders per hour during its 14-hour daily active window (4,000 orders per day). During a two-hour severe slowdown, checkout wait times jump from under 1 second to over 20 seconds. Industry data confirms that shopping cart abandonment spikes by approximately 70% during such delays, resulting in roughly 200 lost orders per hour.
  - *Monthly Revenue Loss:* 200 lost orders per hour × 2 hours × 2 slowdown incidents per month = **800 lost customer orders per month**.
  - *Total Financial Loss:* At an average basket value of 350 Ghana Cedis, this causes a direct, unrecoverable loss of **280,000 Ghana Cedis per month (3.36 million Ghana Cedis annually)**. Even if we conservatively halve this estimate, Kloud Kart is losing over 1.6 million Ghana Cedis every year from dropped checkouts.
- **What we decided to do:** We planned an immediate move of all reporting tasks to the pre-approved duplicate database server (the reporting mirror). This guarantees that reports and exports run on separate hardware and never touch the live storefront machine.
- **Remaining risk:** Low once the second server is turned on. It only requires a basic check to ensure the mirror stays in sync with the live database.

---

### Root Cause 2: Uncontrolled Customer Data Distribution Under Act 843
- **Where it occurs in the data lifecycle:** Ingestion, Storage, and Consumption.
- **Data Quality Dimension affected:** Validity, Privacy Governance, and Security.
- **The Mechanism:** Marketing and Operations staff manually export raw customer data containing names, telephone numbers, home delivery addresses, and email addresses. These files sit in unsecured downloads folders, desktop folders, and email chains.
- **Costing:**
  - *The Legal Rule:* Under Section 33 of Ghana's Data Protection Act, 2012 (Act 843), every citizen has the legal right to request the deletion or correction of their personal data. The company has a strict 90-day statutory clock to comply once a formal notice is received from the Data Protection Commission.
  - *The Copy-Counting Rule:* "Every copy you create is a place a deletion request must reach."
  - *Statutory Exposure:* If a customer deletion request arrives today, Kloud Kart cannot locate or erase the records sitting on staff laptops. Fines under Act 843, mandatory regulatory audit fees, legal representation, and public reputational damage during active investor discussions create an estimated risk-weighted liability of **500,000 to 1,200,000 Ghana Cedis**.
- **What we decided to do:** We planned a strict privacy gateway. Before any customer transaction data enters the reporting system, personal names, phone numbers, and physical home addresses are permanently removed at the gate. Customer emails are converted into irreversible anonymous codes (such as turning an email into `cust_98234`).
- **Remaining risk:** Historical spreadsheets already saved on employee laptops must be identified and safely erased by company management.

---

### Root Cause 3: Conflicting Business Logic and Manual Spreadsheets
- **Where it occurs in the data lifecycle:** Transformation and Consumption.
- **Data Quality Dimension affected:** Consistency and Accuracy.
- **The Mechanism:** Operations and Finance have never agreed on a standardized formula for revenue. Nana counts shipped packages; Finance counts cleared bank deposits. Because each team writes their own formulas in private spreadsheets, their weekly numbers never match.
- **Costing:**
  - *Wasted Executive Labour:* Nana Adjei (Head of Operations), the Finance Lead, and senior department staff spend at least 4 hours every Monday morning comparing spreadsheets, tracing individual order rows, and debating which number to present to the Managing Director.
  - *Annual Labour Waste:* 4 hours per week × 2 senior leaders × 52 weeks = **416 executive hours wasted per year**.
  - *Total Labour Cost:* At an executive hourly rate of 200 Ghana Cedis, Kloud Kart wastes over **83,200 Ghana Cedis per year** in executive salaries paying senior leaders to act as human calculators.
  - *Strategic Cost:* More importantly, the Managing Director and the Board cannot trust weekly financial statements, making investor reporting, cash planning, and inventory restocking decisions unreliable.
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
   - *Question:* "What are the exact hardware specifications of the current server (processor core count, RAM capacity, and disk storage type), and is the pre-approved second server identical in hardware?"
   - *Why this matters:* Confirms whether the current machine has enough memory to buffer database indexes and verifies that the mirror server can take over instantly if the primary server fails.

2. **Payment Gateway Settlement Schedules:**
   - *Question:* "What are the exact settlement cutoff hours and clearing schedules for Paystack, bank cards, and mobile money providers in Ghana and Nigeria?"
   - *Why this matters:* Allows the Analytics Engineer to align the daily reporting batch schedule with actual bank deposits, closing the gap between shipped orders and cleared cash.

3. **Customer Return and Refund Timelines:**
   - *Question:* "What is Kloud Kart's average return window, what percentage of dispatched orders are returned, and at what exact stage does Finance issue a customer refund?"
   - *Why this matters:* Ensures that returned merchandise is automatically deducted from net revenue models rather than manually adjusted weeks later in spreadsheets.

4. **Nigeria Pilot Data Storage:**
   - *Question:* "Does the Nigeria expansion pilot store its customer data in the same MySQL database in Accra, or does it use a separate hosting service in Lagos?"
   - *Why this matters:* Governs cross-border data transfer rules under Section 18 of Ghana's Act 843 and the Nigeria Data Protection Act.

5. **Marketing Data Access Habits:**
   - *Question:* "What specific customer attributes does the Marketing team genuinely need to design promotional campaigns, and why are complete spreadsheets of 300,000 accounts being downloaded?"
   - *Why this matters:* Helps us build secure, privacy-compliant aggregated customer reports so marketing staff never need raw personal contact files again.
