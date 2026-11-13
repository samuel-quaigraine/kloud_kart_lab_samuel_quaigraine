# Kloud Kart: Twelve-Month Data Strategy and System Architecture
## Detailed Executive Presentation Guide and Board Briefing

**Source Presentation Deck:** [presentation/board_presentation.pptx](board_presentation.pptx)  
**Presenter:** Nana Adjei, Head of Operations  
**Audience:** Board of Directors and Investor Representatives  
**Organization:** Kloud Kart (Accra, Ghana)  
**Date:** Friday, November 13, 2026  
**Context:** Twelve-Month Post-Funding Data Strategy and Headcount Allocation  

---

## Slide 1: Fixing Our Data Foundation for Growth

- **Category Kicker:** `BOARD OF DIRECTORS STRATEGY BRIEFING`
- **Slide Title:** Fixing Our Data Foundation for Growth
- **Visual Layout Archetype:** Executive Title Slide with Dark Navy Hero Container and Brand Accents (Widescreen 16:9).

### On-Slide Visual Content
```
========================================================================================
                         BOARD OF DIRECTORS STRATEGY BRIEFING
                         Fixing Our Data Foundation for Growth
                                      Kloud Kart
                         Nana Adjei, Head of Operations
                           Friday, November 13, 2026
========================================================================================
```

### Detailed Business Context and Engineering Mechanism
- **Company Scale:** Kloud Kart is a three-year-old online retailer based in Accra, Ghana, shipping approximately 4,000 orders per day across Ghana with an active pilot expansion in Nigeria.
- **Operating Growth:** The company has delivered consistent 15% to 20% annual top-line growth and recently closed a funding round with investor expectations for a credible, scalable data strategy.
- **Technical Footprint:** Orders, inventory, and customer accounts live in a single MySQL database (~40 gigabytes total footprint) hosted on the exact same server hardware as the customer-facing PHP storefront.
- **Staffing Capacity:** The business operates with exactly one PHP/MySQL software developer and zero specialized data engineers.
- **Executive Mandate:** Nana Adjei is non-technical. The board presentation must explain the engineering strategy, business justification, and regulatory safeguards in plain, accessible language without technical jargon.

### Nana Adjei's Spoken Presentation Script (Speaker Notes)
> *"Members of the board, welcome. Kloud Kart is in a strong commercial position. We are shipping 4,000 orders every day, piloting in Nigeria, and growing 15% to 20% year over year. However, our operating systems are feeling severe strain. Our live store and our database share a single machine. When I run weekly reports, our website freezes for shopping customers. When Finance and I meet on Mondays, we spend hours debating conflicting sales numbers. Today, I am presenting a practical, right-sized data plan that fixes these problems permanently, protects our customers under Ghana's privacy laws, and stays strictly within our approved two-person hiring budget."*

### Anticipated Board and Investor Questions and Answers
- **Q1: Why are we presenting a data strategy now rather than waiting for next fiscal year?**  
  *Nana's Answer:* "Because our shared server is already causing customer cart abandonment during peak hours, and unmanaged customer spreadsheets on employee laptops create urgent regulatory exposure under Ghana's Data Protection Act. We must fix our data foundation now so expansion does not amplify operational losses."
- **Q2: Who will lead execution if Nana is Head of Operations and not a software engineer?**  
  *Nana's Answer:* "I own operational governance and delivery accountability. In Month 1, we hire an experienced Data Engineer to execute the technical plumbing, followed by an Analytics Engineer in Month 3 to standardize reporting models."

---

## Slide 2: Three Urgent Problems Holding Us Back

- **Category Kicker:** `CURRENT OPERATIONAL STRAIN`
- **Slide Title:** Three Urgent Problems Holding Us Back
- **Visual Layout Archetype:** Three-Card Problem Grid with Alert Accents (Widescreen 16:9).

### On-Slide Visual Content
```
========================================================================================
                              CURRENT OPERATIONAL STRAIN
                        Three Urgent Problems Holding Us Back
----------------------------------------------------------------------------------------
 [CARD 1: Monday Site Slowdowns]      [CARD 2: Conflicting Revenue]       [CARD 3: Privacy Exposure]
 Weekly report exports freeze live    Operations and Finance report       Customer spreadsheets sit
 checkout during peak shopping.       different weekly totals.            on staff laptops.
========================================================================================
```

### Detailed Business Context and Engineering Mechanism
Each of the three symptoms is rooted in a specific physical system failure costed below:

| Symptom & Card | Underlying Technical Mechanism | Quantified Business & Financial Impact |
|---|---|---|
| **Card 1: Monday Site Slowdowns** | Heavy weekly reporting exports run directly against the live MySQL database, causing extensive row locks and CPU saturation. | During 08:00 to 10:00 AM Monday peak shopping, customer checkout wait times spike from <1s to >20s, triggering an estimated 70% cart abandonment spike. This costs approximately **200 lost orders/hour, or ~800 lost orders per month (~280,000 Ghana Cedis monthly top-line loss; ~3.36 million Ghana Cedis annually)**. *(Detailed in situation_diagnosis.md Section 3).* |
| **Card 2: Conflicting Revenue** | Neither team works from a shared, written definition of revenue. Operations counts placed warehouse orders; Finance counts cleared bank settlements. | Nana and the Finance Lead spend an average of 4 hours every Monday reconciling spreadsheet rows. This wastes **416 senior leadership hours annually (~83,200 Ghana Cedis in wasted leadership payroll)** and delays executive decision-making. |
| **Card 3: Legal Privacy Exposure** | Staff across Operations, Finance, and Marketing routinely download customer lists (~300,000 records) into untracked spreadsheet files on personal laptops. | Creates acute compliance exposure under Section 33 of Ghana's Data Protection Act, 2012 (Act 843). Kloud Kart faces an active Data Protection Commission complaint with a strict 90-day internal implementation deadline to prove full-system erasure, carrying an illustrative risk-weighted exposure of **500,000 to 1,200,000 Ghana Cedis**. |

### Nana Adjei's Spoken Presentation Script (Speaker Notes)
> *"These three issues are not minor operational inconveniences; they are actively costing us revenue, leadership time, and legal standing. Twice last month, Monday reporting queries slowed our storefront to a crawl, causing an estimated loss of 800 customer orders. Between Finance and Operations, we lose ten full working weeks every year manually cross-checking spreadsheet rows. Furthermore, having customer lists on staff laptops leaves us exposed under Ghana's Data Protection Act while we work through an active complaint forwarded by the Data Protection Commission. Doing nothing is our most expensive option."*

### Anticipated Board and Investor Questions and Answers
- **Q1: How was the 280,000 Ghana Cedis monthly lost sales figure calculated?**  
  *Nana's Answer:* "Kloud Kart averages 285 orders per hour across its 14-hour daily window. During two-hour checkout freezes, checkout wait times exceed 20 seconds, producing an estimated 70% cart abandonment spike (~200 lost orders per hour). At an average basket value of 350 Ghana Cedis across two monthly incidents, that models 280,000 Ghana Cedis in lost revenue."
- **Q2: Why can't Nana and Finance simply agree on a spreadsheet formula today?**  
  *Nana's Answer:* "Because we pull separate data exports at different times into private spreadsheets. Without an automated, centralized database calculation, any manual spreadsheet agreement breaks down the following week."

---

## Slide 3: Sized for Our Real Scale, Not Amazon's

- **Category Kicker:** `RIGHT-SIZED ARCHITECTURE`
- **Slide Title:** Sized for Our Real Scale, Not Amazon's
- **Visual Layout Archetype:** Metric Hero Callout Card with Side-by-Side Narrative (Widescreen 16:9).

### On-Slide Visual Content
```
========================================================================================
                               RIGHT-SIZED ARCHITECTURE
                        Sized for Our Real Scale, Not Amazon's
----------------------------------------------------------------------------------------
                                       [ 40 GB ]
                           Our Entire Company Data Footprint
    4,000 daily orders fit easily on our pre-approved second server without costly
                                   cloud platforms.
========================================================================================
```

### Detailed Business Context and Engineering Mechanism
- **The Over-Engineering Trap:** Well-meaning advisors often recommend buying enterprise cloud platforms like Snowflake, BigQuery, or Databricks, or building a complex data lakehouse.
- **Physical Reality of 40 Gigabytes:** Kloud Kart's entire three-year operational history totals approximately 40 gigabytes. Forty gigabytes fits entirely inside the memory (RAM) of a single modern commercial server.
- **Cost and Operational Comparison:**

| Architectural Option | Monthly Infrastructure Cost | Staffing Requirements | Organizational Fit |
|---|---|---|---|
| **Enterprise Cloud Warehouse (Snowflake / BigQuery)** | Unpredictable metered bills ($1,500 to $4,000+ per month) due to query compute spikes. | Requires specialized cloud data engineers and dedicated infrastructure specialists. | **Poor:** Expensive over-engineering for a 40 GB relational footprint. |
| **Data Lakehouse (Parquet / Object Storage)** | Complex multi-tier storage licensing. | Requires Python/Spark software engineers. | **Poor:** Adds fragile pipeline complexity without business benefit. |
| **Dedicated Relational Server (Pre-Approved Server 2)** | **0 Ghana Cedis new server cost** (already pre-approved in budget); under 800 GHS/month for dashboard tools. | Operable by one Data Engineer and one Analytics Engineer. | **Optimal (ADR-002):** Fast, predictable, and fully sized for our scale. |

### Nana Adjei's Spoken Presentation Script (Speaker Notes)
> *"When companies raise capital, the immediate temptation is to buy expensive enterprise software like Snowflake or build a massive cloud lakehouse. For Kloud Kart, that would be an expensive mistake. Our entire database is 40 gigabytes. That fits easily into standard computer memory. Buying cloud platforms would introduce unpredictable monthly invoices and require specialist engineers we cannot afford. Instead, we use our pre-approved duplicate server to run clean reporting tables, keeping operating costs low and predictable."*

### Anticipated Board and Investor Questions and Answers
- **Q1: Will a 40-gigabyte relational architecture support our 15% to 20% annual growth?**  
  *Nana's Answer:* "Yes. At 20% annual growth, our database will add roughly 8 to 10 gigabytes per year. Modern relational database servers easily handle hundreds of gigabytes before requiring architectural re-evaluation."
- **Q2: If an investor insists on Snowflake because other portfolio companies use it, what is our response?**  
  *Nana's Answer:* "We explain that cloud warehouses charge per query byte scanned. For 4,000 daily orders, our second server delivers identical sub-second dashboard performance at zero added hardware cost, protecting investor capital for customer acquisition."

---

## Slide 4: Separating Live Checkout from Daily Reports

- **Category Kicker:** `HOW IT WORKS`
- **Slide Title:** Separating Live Checkout from Daily Reports
- **Visual Layout Archetype:** Before-and-After Transformation Container (Split Two-Column Layout, Widescreen 16:9).

### On-Slide Visual Content
```
========================================================================================
                                      HOW IT WORKS
                     Separating Live Checkout from Daily Reports
----------------------------------------------------------------------------------------
   BEFORE: ONE SHARED BOX                               AFTER: TWO DEDICATED SERVERS
   Reports Fight Shoppers for Speed                     Live Store Stays Fast 24/7
   --------------------------------                     --------------------------
   • Shared Server: Live store and customer             • Server 1 (Live Shop): Serves customer
     data share one box.                                  orders and live stock only.
   • Peak Delays: Monday downloads freeze               • Server 2 (Replica): Runs all team
     customer checkout.                                   reports and Finance checks.
   • Manual Files: Staff export raw spreadsheet         • Zero Slowdowns: Heavy reports never
     files to personal laptops.                           touch the live storefront.
========================================================================================
```

### Detailed Business Context and Engineering Mechanism
- **The Core Problem:** The storefront website and internal analytical queries compete for the same physical processor cores, disk I/O channels, and memory buffers on Server 1.
- **The Architectural Solution (ADR-001):**
  1. **Activate Server 2:** Configure the pre-approved duplicate server as an automated, read-only mirror (read replica) of Server 1 using standard MySQL replication.
  2. **Workload Isolation:** Customer shopping checkouts write exclusively to Server 1. All analytical reads, Monday exports, and Finance audits execute exclusively against Server 2.
  3. **Fault Isolation:** Even if an internal team runs an unindexed query scanning millions of rows on Server 2, Server 1 remains 100% responsive, keeping customer checkout page latency below two seconds.

### Nana Adjei's Spoken Presentation Script (Speaker Notes)
> *"Here is how we fix our website slowdowns immediately. Today, our shoppers and our reporting queries share one server box. When I export Monday numbers, customer checkouts stall. Our solution activates our pre-approved second server as a duplicate mirror. Online shoppers place orders on Server 1, while internal reports and Finance audits read from Server 2. The live store stays fast 24 hours a day, and reports never slow down customer checkouts again."*

### Anticipated Board and Investor Questions and Answers
- **Q1: What happens if the automated replication between Server 1 and Server 2 lags?**  
  *Nana's Answer:* "Because standard company reports refresh once daily at 02:00 AM, a replication lag of a few minutes has zero impact on daily reporting. Live warehouse checkout checks remain on Server 1, ensuring stock accuracy is never affected."
- **Q2: Does activating Server 2 require purchasing any new hardware?**  
  *Nana's Answer:* "No. Server 2 is already provisioned and pre-approved in our current operational budget."

---

## Slide 5: Meeting Our 90-Day Customer Deletion Deadline

- **Category Kicker:** `GHANA DATA PROTECTION ACT (ACT 843)`
- **Slide Title:** Meeting Our 90-Day Customer Deletion Deadline
- **Visual Layout Archetype:** Three-Step Process Sequence with Compliance Callout (Widescreen 16:9).

### On-Slide Visual Content
```
========================================================================================
                         GHANA DATA PROTECTION ACT (ACT 843)
                   Meeting Our 90-Day Customer Deletion Deadline
----------------------------------------------------------------------------------------
   [ 01: Strip Personal Details ]       [ 02: Keep Safe Sales Facts ]       [ 03: Erase or Restore in One Place ]
   Names, phones, and addresses         Order totals and delivery           Customer deletions or restoring
   removed before reporting.            regions remain for reporting.       require changing one record.
========================================================================================
```

### Detailed Business Context and Engineering Mechanism
- **Statutory Legal Context:** Under Section 33 of Ghana's Data Protection Act, 2012 (Act 843), individuals have the statutory right to request erasure of their personal data, with standard regulatory compliance expected within 21 calendar days.
- **The Active Regulatory Complaint:** Kloud Kart faces an active complaint forwarded by the Data Protection Commission regarding a customer's deleted data, operating under a strict 90-day internal implementation deadline to prove full-system erasure and compliant data controls.
- **Three-Step Privacy Engineering Architecture (ADR-004):**
  1. **Pre-Load Data Scrubbing (Step 01):** Direct personal identifiers (customer full names, phone numbers, and physical home addresses) are permanently stripped before data enters the reporting schema.
  2. **One-Way Anonymization (Step 02):** Customer email addresses are converted into irreversible anonymous reference codes (e.g. `cust_98234`), preserving repeat purchase analytics and cohort tracking without exposing personal contact details.
  3. **Permanent 6-Year Deletion Audit Log & Dual-Path Protocol (Step 03):** Every customer deletion or restoration is recorded in `AUDIT_CUSTOMER_DELETION_LOG` (retained for 6 years, accessible only to Nana Adjei and the lead database engineer, with read-only inspection access for official auditors). This automatically re-applies deletions to restored system backups so erased records never return (removing), while permitting targeted recovery of purchase history via surrogate keys if an account was closed or contested in error (restoring).

### Nana Adjei's Spoken Presentation Script (Speaker Notes)
> *"Under Ghana's Data Protection Act, customers have the legal right to request that we delete their personal information. Today, because customer lists sit in untracked spreadsheets on staff laptops, we cannot prove that records are truly erased. Our architecture solves this in three clear steps. First, we strip personal names, phone numbers, and addresses at the gate before data enters reporting tables. Second, we keep anonymous purchase totals so sales analysis remains 100% accurate. Third, we log every deletion in a permanent audit log retained for six years, ensuring restored backup files never bring back erased records, while still allowing us to recover past order history if an account was closed by mistake."*

### Anticipated Board and Investor Questions and Answers
- **Q1: How does this solve our active Data Protection Commission complaint within 90 days?**  
  *Nana's Answer:* "In Quarter 1, we eliminate unmanaged spreadsheet files from laptops, deploy the automated privacy gateway, and run a certified audit drill proving full-system erasure, providing verified documentation to settle the complaint."
- **Q2: If customer contact details are stripped, how does Marketing evaluate customer cohorts?**  
  *Nana's Answer:* "Marketing analyzes customer behavior through anonymous reference codes. They can measure repeat purchase frequency, order value, and product category trends without ever seeing raw personal names or phone numbers."

---

## Slide 6: Daily Updates for Reports, Live Checks for Stock

- **Category Kicker:** `SMART REFRESH SPEED`
- **Slide Title:** Daily Updates for Reports, Live Checks for Stock
- **Visual Layout Archetype:** Dual Workload Split Card (Batch vs. Real-Time, Widescreen 16:9).

### On-Slide Visual Content
```
========================================================================================
                                   SMART REFRESH SPEED
                   Daily Updates for Reports, Live Checks for Stock
----------------------------------------------------------------------------------------
        [ ONCE DAILY: Operations, Finance & Marketing ]
        Automatic daily updates avoid costly 24/7 streaming servers.
        
        [ REAL-TIME: Warehouse Physical Stock ]
        Live checkout checks prevent selling out-of-stock items.
========================================================================================
```

### Detailed Business Context and Engineering Mechanism
- **The Myth of Real-Time Analytics:** Continuous real-time streaming pipelines (e.g. Apache Kafka, Flink) across an entire company database require complex infrastructure and round-the-clock engineering maintenance.
- **The Pragmatic Workload Split (ADR-003):**
  - **99% Daily Batch Reporting (02:00 AM Nightly):** Financial reconciliation, marketing performance, regional analysis, and executive KPIs refresh automatically once every 24 hours at 02:00 AM on Server 2. Yesterday's confirmed numbers are stable, verified, and completely free of mid-day drift.
  - **The 1% Operational Exception (Live Warehouse Stock):** When an online shopper checks out on the website, inventory stock balances are validated live on Server 1. This guarantees that customer checkout never sells items that are out of stock.
  - **On-Demand Stock Drift Checks:** Warehouse supervisors can initiate on-demand stock drift comparisons on Server 2 during flash sales or payday trading weekends, identifying physical inventory shrinkage without creating load on the live store.

### Nana Adjei's Spoken Presentation Script (Speaker Notes)
> *"Investors frequently ask if we are building a real-time streaming pipeline. The honest operational truth is that only our warehouse stock balance needs real-time validation, so shoppers cannot buy out-of-stock items. For everything else (financial totals, marketing metrics, and regional sales reports), refreshing once a day at 02:00 AM is 100% sufficient. Executive decisions do not change minute by minute; yesterday's verified numbers are cheaper, cleaner, and far more dependable."*

### Anticipated Board and Investor Questions and Answers
- **Q1: Why not build a streaming pipeline now to future-proof our infrastructure?**  
  *Nana's Answer:* "Streaming infrastructure introduces high maintenance costs and software complexity that our two data hires would spend all their time debugging. Sizing for daily batch keeps our team focused on high-value business reporting."
- **Q2: What happens if physical warehouse stock drifts during daytime operations?**  
  *Nana's Answer:* "Our nightly batch script compares physical warehouse scan logs against database balances, alerting warehouse staff at 08:00 AM to correct discrepancies before customer orders are impacted."

---

## Slide 7: Two Focused Hires, Zero Unneeded Roles

- **Category Kicker:** `STAFFING WITHIN BUDGET`
- **Slide Title:** Two Focused Hires, Zero Unneeded Roles
- **Visual Layout Archetype:** Two-Hire Sequencing Cards with Explicit Non-Hiring Callout Banner (Widescreen 16:9).

### On-Slide Visual Content
```
========================================================================================
                                STAFFING WITHIN BUDGET
                        Two Focused Hires, Zero Unneeded Roles
----------------------------------------------------------------------------------------
 [CALLOUT BANNER]: What we are NOT hiring: No AI or Data Scientist this year:
                   we must clean our core numbers before forecasting.
----------------------------------------------------------------------------------------
 [HIRE 1 • MONTH 1: Data Engineer]                [HIRE 2 • MONTH 3: Analytics Engineer]
 Runs the second server, daily updates,           Unifies revenue formulas and builds
 and privacy scrubbing.                           team dashboards.
========================================================================================
```

### Detailed Business Context and Engineering Mechanism
- **Approved Headcount:** The board has budgeted exactly **two data hires** for this financial year (ADR-005).
- **Sequencing Strategy: Fix Operational Plumbing First, Then Standardize Metrics**

| Role and Sequence | Primary Accountability | 30 / 60 / 90-Day Key Milestones | What They Do NOT Do |
|---|---|---|---|
| **Hire 1: Data Engineer** *(Starts Month 1)* | Data movement, server replication, pipeline automation, and data protection compliance. | **Day 30:** Connect duplicate server mirror; verify storefront loads <2s during Monday reports.<br>**Day 60:** Automate nightly 02:00 AM privacy scrubbing; retire unmanaged laptop spreadsheets.<br>**Day 90:** Activate 6-step deletion protocol and settle Data Protection Commission complaint. | Does not define business metrics or build executive presentation decks. |
| **Hire 2: Analytics Engineer** *(Starts Month 3)* | Business calculation layer, unified metric definitions, and self-service dashboards. | **Day 30 (M4):** Formalize single revenue rule with Nana and Finance in SQL.<br>**Day 60 (M5):** Deploy automated 08:00 AM daily variance alerts.<br>**Day 90 (M6):** Deliver self-service reporting dashboards for Operations, Finance, and Marketing. | Does not build predictive machine learning models or manage physical server infrastructure. |

- **What We Are Deliberately Postponing:** We explicitly reject hiring a Data Scientist or Machine Learning Engineer this year. Forecasting demand on top of uncleaned inventory records and disputed revenue figures produces confident-looking wrong answers. Data integrity comes first; machine learning can be evaluated in Year 2.

### Nana Adjei's Spoken Presentation Script (Speaker Notes)
> *"We have budget for exactly two data hires. We are not hiring an expensive data scientist or artificial intelligence specialist. Predicting demand when our basic stock counts drift and our sales numbers disagree is a waste of capital. In Month 1, we hire a Data Engineer to connect the duplicate server, stop website freezes, and clean customer data. In Month 3, we hire an Analytics Engineer to build the single revenue model that Finance and I agree on. Two hires, zero fluff."*

### Anticipated Board and Investor Questions and Answers
- **Q1: When will Kloud Kart be ready to hire a Data Scientist for demand forecasting?**  
  *Nana's Answer:* "In Year 2, once our single source of truth has operated cleanly for at least six months and our inventory drift is proven to stay below 0.5%."
- **Q2: What happens if recruiting the Data Engineer takes longer than 30 days?**  
  *Nana's Answer:* "We have already drafted the job specification and technical scorecard, focusing on practical MySQL replication and Python skills readily available in the Accra market."

---

## Slide 8: 12-Month Milestones You Can Verify

- **Category Kicker:** `EXECUTION PLAN`
- **Slide Title:** 12-Month Milestones You Can Verify
- **Visual Layout Archetype:** Four-Quarter Delivery Roadmap with Non-Technical Verification Tests (Widescreen 16:9).

### On-Slide Visual Content
```
========================================================================================
                                     EXECUTION PLAN
                           12-Month Milestones You Can Verify
----------------------------------------------------------------------------------------
 [QUARTER 1: Stop Slowdowns]                      [QUARTER 2: One Revenue Number]
 Move reports off live site and meet              Align Operations and Finance totals
 90-day privacy deadline.                         to the exact cedi.
----------------------------------------------------------------------------------------
 [QUARTER 3: Nigeria & Self-Serve]                [QUARTER 4: Stock & Audit Safety]
 Separate Nigeria pilot tracking and              Automate stock mismatch alerts and
 team report views.                               backup deletion checks.
========================================================================================
```

### Detailed Business Context and Engineering Mechanism
Every quarterly milestone includes a non-technical verification test that Nana Adjei and Finance can perform without engineering assistance:

- **Quarter 1 (Months 1 to 3): Website Speed Protected and Customer Data Sanitized**
  - *Business Outcome:* Monday exports move to Server 2, unmanaged customer spreadsheets are deleted from laptops, and the 6-step deletion protocol settles the active Data Protection Commission complaint within the 90-day implementation period.
  - *Non-Technical Verification:* Nana runs the Monday 09:00 AM report while placing a live test checkout; the page loads in under two seconds. Department leads confirm zero customer files remain on laptops, and a test deletion audit verifies full-system erasure.
- **Quarter 2 (Months 4 to 6): Single Source of Truth for Company Revenue**
  - *Business Outcome:* Operations and Finance adopt one shared, locked revenue formula inside the reporting database, ending the weekly reconciliation dispute.
  - *Non-Technical Verification:* On the first Monday of Month 5, Finance and Operations pull their reports from the shared dashboard; the revenue figures match exactly, backed by automated daily warning emails flagging variances at 08:00 AM.
- **Quarter 3 (Months 7 to 9): Separate Nigeria Tracking and Self-Serve Team Reports**
  - *Business Outcome:* Nigeria pilot sales and delivery numbers are tracked separately from Ghana, and department leads pull their own standard reports.
  - *Non-Technical Verification:* Board review displays a dedicated Nigeria view without mixing Ghana totals, and leads run monthly reports without developer help.
- **Quarter 4 (Months 10 to 12): Stock Mismatch Alerts and Permanent Customer Deletions**
  - *Business Outcome:* Automated alerts flag mismatches between website stock counts and physical warehouse shelves before items oversell, and every customer data action is recorded in a permanent audit log so erased customers never reappear after backup restores while allowing targeted recovery if a record was closed or contested by mistake.
  - *Non-Technical Verification:* Overselling cancellations drop below 0.5% of total orders by December 15, and practice backup restore tests verify zero personal records return for deleted customers while accurately logging every action for regulatory audits by December 20.

### Nana Adjei's Spoken Presentation Script (Speaker Notes)
> *"Here is our commitment for the next four quarters. Every milestone can be verified by myself or Finance without asking an engineer. In Quarter 1, the website stops slowing down, unmanaged customer spreadsheets are removed, and we resolve our active privacy complaint within our 90-day implementation period. In Quarter 2, Finance and Operations report identical revenue. In Quarter 3, Nigeria reporting is cleanly isolated and department leads self-serve. In Quarter 4, automated alerts catch stock mismatches before items oversell, and practice backup restore tests prove that deleted customer records stay permanently erased."*

### Anticipated Board and Investor Questions and Answers
- **Q1: What is the single biggest risk to this 12-month delivery timeline?**  
  *Nana's Answer:* "Hiring delay for the Data Engineer in Month 1. We mitigate this by using a standardized practical skills assessment focusing on proven MySQL and Python ingestion experience rather than theoretical algorithms."
- **Q2: Who is responsible for certifying milestone completion at each quarter?**  
  *Nana's Answer:* "I personally verify and sign off on operational outcomes alongside the Finance Lead and Managing Director before reporting to the board."

---

## Slide 9: Three Immediate Actions to Launch

- **Category Kicker:** `BOARD DECISION REQUEST`
- **Slide Title:** Three Immediate Actions to Launch
- **Visual Layout Archetype:** Three-Action Executive Approval Card with Investment Summary (Widescreen 16:9).

### On-Slide Visual Content
```
========================================================================================
                                 BOARD DECISION REQUEST
                           Three Immediate Actions to Launch
----------------------------------------------------------------------------------------
   1. Activate our pre-approved second server
   2. Open hiring for our Data Engineer
   3. Resolve the customer data deletion complaint
========================================================================================
```

### Detailed Business Context and Engineering Mechanism
- **Action 1: Activate Pre-Approved Server 2 (Next 7 Days):** Authorize IT hosting provider to turn on the duplicate database server and configure MySQL replication. (Hardware cost: 0 Ghana Cedis added; pre-approved in budget).
- **Action 2: Open Recruitment for Data Engineer (Next 14 Days):** Release the job description for Hire 1, targeting a start date in Month 1 to execute server replication and privacy pipeline setup.
- **Action 3: Settle Customer Deletion Complaint (Next 90 Days):** Direct department leads across Operations, Finance, and Marketing to execute the 6-step deletion protocol, remove unmanaged files, and file the formal compliance certificate with the Data Protection Commission.
- **Capital and Operational Budget Summary:**
  - *Hardware Infrastructure:* 0 Ghana Cedis new server capital (Server 2 pre-approved).
  - *Software Subscriptions:* Under 800 Ghana Cedis per month for open-source dashboard hosting and automated backup tools.
  - *Headcount:* Exactly two approved data hires within existing fiscal budget.

### Nana Adjei's Spoken Presentation Script (Speaker Notes)
> *"To launch this plan immediately, we require three specific board authorizations today. First, authorize the activation of our pre-approved duplicate server so we can move reporting off the live website. Second, authorize opening recruitment for our Data Engineer starting in Month 1. Third, authorize our 90-day compliance sprint to eliminate unmanaged customer spreadsheets and resolve our Data Protection Commission complaint. This plan solves our real bottlenecks, protects our company legally, respects our budget, and gives us numbers we can trust. Thank you, and I look forward to your questions."*

### Anticipated Board and Investor Questions and Answers
- **Q1: Can we activate the second server before the Data Engineer starts?**  
  *Nana's Answer:* "Yes. Our existing PHP/MySQL developer can configure basic replication with our hosting provider immediately, allowing the Data Engineer to begin pipeline development on Day 1."
- **Q2: What is the formal resolution we are asking the board to adopt?**  
  *Nana's Answer:* "To approve the twelve-month data strategy roadmap, authorize recruitment of Hire 1 (Data Engineer), and ratify the customer data deletion and privacy compliance protocol."
