# Strategic Recommendation: Building a Defensible Data Platform for Kloud Kart

**To:** Nana Adjei, Head of Operations  
**From:** Data Strategy Practice  
**Date:** November 12, 2026  
**Subject:** Twelve-Month Data Strategy, Architecture, and Staffing Recommendation

---

## 1. Executive Position: Sizing for Kloud Kart, Not Amazon

Kloud Kart ships approximately 4,000 orders per day with steady 15% to 20% annual sales growth and operates roughly 40 gigabytes of structured relational data.

Following the recent investment funding round, investors and internal developer discussions suggested building an enterprise data lakehouse, deploying real-time streaming dashboards, and hiring artificial intelligence engineers for machine learning demand forecasting.

**We advise the board to reject these proposals.**

A data lakehouse was designed for giant enterprises storing petabytes of unorganized video, audio, and sensor files. Cloud data warehouses like Snowflake charge metered fees for every second of computer time, which caused the Finance department to flinch. Real-time streaming requires complex 24-hour monitoring that would exhaust a small team. Most importantly, machine learning demand forecasting built on top of conflicting revenue numbers and uncleaned data will merely produce inaccurate forecasts with mathematical confidence.

Kloud Kart does not have a "big data" problem. Kloud Kart has a **data separation and definition problem**.

Our recommendation commits to an architecture with the smallest number of moving parts that stops site slowdowns, unifies company revenue reporting, complies with Ghanaian privacy law, and can be operated reliably by a two-person data team.

---

## 2. The Architectural Strategy

```
[Shoppers] ---> [Online Web Store] <---> [Primary MySQL Database: Server 1]
                                                 |
                                     (Automated Real-Time Mirror)
                                                 v
                                   [Duplicate Server: Server 2 (Read Replica)]
                                   - Raw Replicated Tables (Mirror)
                                   - Nightly Ingestion & PII Sanitization
                                   - Clean Reporting Schema & Marts (Pre-Packaged metrics)
                                                 |
                                  (Standardized SQL Queries)
                                                 v
                              [Unified Dashboards: Operations & Finance]
```

### Component 1: Workload Isolation via the Duplicate Database Server

- **The Decision:** Deploy the pre-approved second server as an automated, read-only mirror (read replica) of the primary MySQL database.
- **Why It Works:** Shoppers interact exclusively with the primary database. All heavy reporting queries, weekly exports, and internal analytics are redirected to the duplicate server.
- **The Business Outcome:** The Monday morning website slowdowns that crippled the store twice last month are permanently eliminated. The live website remains responsive regardless of analytical activity.

### Component 2: Two-Step Privacy Sanitization and Query Loading

- **The Decision:** Rather than dumping raw personal customer records into an unmonitored repository or maintaining separate physical database boxes, we implement privacy cleaning directly on the second server:
  1. _Step 1 (Sanitization at the Gate):_ As data is extracted from the duplicate server, an automated process strips away direct customer identifiers (names, mobile phone numbers, and physical street addresses). Customer email addresses are converted into irreversible anonymous account codes (such as `cust_98234`).
  2. _Step 2 (Flexible Query Calculations):_ All business transaction facts (quantities, item prices, order timestamps, and cedi values) land in a dedicated reporting schema on that same second server. Business definitions are written as standardized database queries in SQL.
- **Why It Works:** As I understand Act 843, individuals have the statutory right to request deletion of their personal data (with standard turnaround guidelines requiring action within 21 calendar days). Kloud Kart faces an active Data Protection Commission complaint regarding a deleted customer's data. This complaint carries dual operational interpretations: either an unfulfilled deletion request leaving lingering copies across laptops (requiring irreversible removal and proof of erasure), or an erroneous deletion where an account was closed by mistake or resurrected during backup restoration (requiring targeted recovery and audit proof). Leadership has established an internal 90-day implementation period to prove full-system erasure, establish targeted recovery safeguards, and achieve repeatable ongoing compliance. Because every copy we create is a place a deletion request must reach, stripping names, phone numbers, and street addresses at the gate keeps personal details out of our reporting schema. Combined with a permanent deletion audit log, this ensures customer deletions only touch the primary database, with automated re-application during backup restores so historical snapshots never resurrect erased data (removing), while permitting targeted recovery of transaction history if an account is contested or flagged in error (restoring). Kloud Kart drastically limits its regulatory audit footprint, prepares for its mandatory Data Protection Commission registration renewal (required every two years as I understand Act 843), and evaluates regional records under core statutory security principles while preserving complete flexibility to adjust business calculations without touching the live shop.

### Component 3: Daily Scheduled Updates with One Named Real-Time Exception

- **The Decision:** Ninety-nine percent (99%) of analytical reporting will refresh once every 24 hours on an automated nightly schedule (running at 02:00 AM). The **single exception** is physical warehouse stock counts, which remain live and transactional on the primary database during checkout, supplemented by nightly stock drift audits that alert warehouse staff to discrepancies before morning business.
- **Why It Works:** We apply the operational test: _"What business decision changes if this number is 10 seconds old instead of 24 hours old?"_ Strategic marketing evaluations, monthly financial ledgers, and regional sales trends do not require sub-second updates; yesterday's complete numbers are 100% sufficient. Conversely, inventory stock counts cannot go stale; even a five-minute delay risks selling items not on the warehouse shelf, triggering refunds and customer frustration. Live stock reservations stay on the primary database, while nightly batch drift audits catch shelf discrepancies before shoppers place orders.

---

## 3. Team Structure and First 90 Days

The board has budgeted **two data hires** for this financial year. We sequence these hires to stop operational loss first before standardizing reporting:

| Role and Sequence                          | Primary Accountability                                                                                         | First 90 Days Deliverable                                                                                                                         | What They Do NOT Do                                                                |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Hire 1: Data Engineer** _(Month 1)_      | Data movement, server replication, pipeline automation, and data protection compliance.                        | Connect the duplicate server replica, automate the nightly transfer script, mask personal customer data, and eliminate manual Monday CSV exports. | Does not define business metrics or build executive presentation slides.           |
| **Hire 2: Analytics Engineer** _(Month 3)_ | The business calculation layer inside the reporting database, metric definitions, and self-service dashboards. | Deliver a single standardized revenue model agreed upon by Nana and Finance, eliminating the weekly Monday reporting discrepancy.                 | Does not build predictive machine learning models or manage server infrastructure. |

### What We Are Choosing NOT to Staff: Data Scientist / Artificial Intelligence

We explicitly advise against hiring a Data Scientist or Artificial Intelligence Engineer this year. Predictive modeling requires trustworthy, stable historical data. Forecasting customer demand on top of uncleaned inventory records and disputed revenue numbers is an expensive distraction. Kloud Kart will establish a single source of truth first. Machine learning can be evaluated in year two once data integrity is proven.

---

## 4. Financial Costs and Resource Justification

- **Hardware Infrastructure:** The duplicate server (read replica) is already pre-approved in the company budget. Storing clean reporting tables in a dedicated reporting schema on this second server requires **zero additional database servers**, saving unnecessary cloud infrastructure costs.
- **Software Licensing:** Zero proprietary vendor lock-in. Built entirely on robust, open-source standards (MySQL replication, Python ingestion, standard SQL, and open-source dashboard tooling such as Metabase).
- **Return on Investment:**
  1. Recovers **416 hours per year** of senior leadership time previously wasted on manual spreadsheets.
  2. Protects an estimated 280,000 Ghana Cedis per month in customer orders previously lost during Monday website slowdowns.
  3. Substantially reduces regulatory exposure under Act 843 (as I understand it) by retiring unmanaged customer CSV spreadsheets.

---

## 5. Direct Answers to Hard Investor Questions

When presenting this strategy to the board, Nana can deliver these direct, plain-language answers to common investor questions:

- **Q1: "Why aren't we building a modern data lakehouse or buying Snowflake or BigQuery?"**  
  _Answer:_ At 4,000 orders per day (~40 gigabytes total data), enterprise cloud warehouses charge metered compute fees that spike unpredictably, and lakehouses require a dedicated specialist team. A simple reporting mirror handles ten times our current volume on predictable infrastructure at a fraction of the cost.
- **Q2: "Another portfolio company has real-time dashboards; why are we refreshing daily?"**  
  _Answer:_ Only live warehouse stock needs instant updates so we don't oversell items on the shelf. Marketing spend, regional sales, and weekly financial totals don't change decisions minute by minute; yesterday's verified numbers are faster, cheaper, and cleaner.
- **Q3: "When will we use AI or machine learning for demand forecasting?"**  
  _Answer:_ In Year 2, after we fix our underlying data. Forecasting demand on top of disputed revenue totals and unchecked stock counts would produce confident-looking wrong answers.
