# Kloud Kart: Twelve-Month Data Plan and System Design

> **Project:** AmaliTech Data Engineering Foundations (DE01) Lab  
> **Client:** Nana Adjei, Head of Operations, Kloud Kart (Accra, Ghana)  
> **Author:** Samuel Quaigraine  
> **Status:** Final Submission for Executive Review and Board Approval

---

## 1. Overview: The Problem and Our Plan

Kloud Kart is a three-year-old online store in Accra, Ghana, shipping about **4,000 orders per day** with a **40-gigabyte MySQL database** and a new expansion pilot in Nigeria.

Right now, the live website and the database share a **single server**, maintained by **one developer**. That setup causes three serious business problems:

1. **Monday Morning Site Slowdowns:** Running heavy weekly reports directly on the live database slows down customer checkouts during peak morning shopping hours, causing checkout delays to jump from under 1 second to over 20 seconds and leading to an estimated loss of 800 customer orders per month (detailed in the [Root Cause 1 Measurement Report](situation_diagnosis.md#3-costing-the-root-causes-three-types-of-financial-impact)).
2. **Conflicting Revenue Numbers:** Operations and Finance calculate weekly revenue in separate spreadsheets with different formulas, so their totals never match.
3. **Uncontrolled Customer Data Copies:** Staff across Operations, Finance, and Marketing routinely export customer lists (estimated at 300,000 records) into untracked spreadsheets on personal laptops. Under Section 33 of Ghana's Data Protection Act, 2012 (Act 843), customers have the statutory right to request the deletion of their personal data, with standard regulatory compliance expected within 21 calendar days. Kloud Kart faces an active complaint forwarded by the Data Protection Commission, operating under a strict 90-day internal implementation period to remove unmanaged laptop files and prove full-system erasure.

### What We Decided to Build

Instead of buying expensive cloud data warehouses, we designed a simple, defensible architecture with five clear decisions documented in our Architecture Decision Records (ADR-001 through ADR-005):

- **Isolate Reporting Workloads (ADR-001):** We activate the pre-approved second server as a read-only mirror of the live store database, moving all heavy reporting queries off the live website so customer checkouts are never slowed down.
- **Relational Reporting Schema (ADR-002):** We store clean analytical tables inside a dedicated schema on that same second server, avoiding costly cloud platform fees and unneeded software complexity.
- **Live Inventory Checkout with Nightly Reporting (ADR-003):** Physical warehouse stock balances remain live on the main store database during checkout to prevent overselling, while all other company reports refresh once every 24 hours at 02:00 AM.
- **Pre-Load Privacy Gateway and Audit Logging (ADR-004):** Direct customer identifiers (names, phone numbers, and physical street addresses) are permanently removed before data enters reporting tables, while customer emails are converted into anonymous reference codes. Every customer deletion is recorded in a permanent audit log retained for six years to meet statutory audit requirements. Access to this log is restricted to the Head of Operations (Nana Adjei) and the lead database engineer, with read-only inspection access granted to official Data Protection Commission auditors.
- **Two-Stage Hiring Sequence (ADR-005):** We hire a Data Engineer in Month 1 to stop website slowdowns and automate data cleaning, followed by an Analytics Engineer in Month 3 to build verified sales dashboards, staying strictly within the board's two-person hiring budget.

---

## 2. Guide to the Files in This Repository

| File | What It Delivers | Primary Business Value |
| :--- | :--- | :--- |
| [situation_diagnosis.md](situation_diagnosis.md) | Separates symptoms from root causes, prices retail losses, and ranks board risks. | Identifies why site slowdowns occur and justifies the investment needed to fix them. |
| [recommendation.md](recommendation.md) | Sized for 40 gigabytes, explains the two-server architecture, 30/60/90-day hiring goals, and investor answers. | Provides Nana with an affordable, defensible technical recommendation for the board. |
| [roadmap.md](roadmap.md) | One-page quarterly plan with non-technical verification tests for every outcome. | Gives leadership visible, quarterly milestones they can verify without engineering help. |
| [decisions/](decisions/) (5 ADRs) | Five formal Architecture Decision Records strictly following the standard house template, evaluating real alternatives and pricing mistakes. | Documents why we chose a simple relational setup over expensive cloud platforms. |
| [presentation/](presentation/) ([.pptx](presentation/board_presentation.pptx), [.md](presentation/board_presentation.md), [.txt](presentation/board_presentation.txt)) | Executive 9-slide presentation provided in visual PowerPoint, formatted Markdown, and plain text formats with complete speaker notes. | Equips Nana to present the plan confidently to investors and the board. |
| [improvement.md](improvement.md) | Explains the built customer data register and Monday revenue sign-off tool. | Recovers 416 hours of executive time annually and provides tangible regulatory proof. |
| [customer_data_inventory_and_deletion_register.md](customer_data_inventory_and_deletion_register.md) | Operational tool tracking five copy locations, 6-step deletion protocol, and weekly revenue sign-off ledger. | Gives operations immediate control over laptop files and stops weekly sales debates. |
| [erd_and_architecture.md](erd_and_architecture.md) | Visual database diagrams and data flow blueprints showing how records move securely. | Provides an auditable technical map of the data pipeline and privacy gateway. |

---

## 3. Executive Board Presentation: Slide Outline and Speaker Summary

For complete reviewability directly in the repository browser, the presentation is provided in visual PowerPoint ([presentation/board_presentation.pptx](presentation/board_presentation.pptx)), formatted Markdown ([presentation/board_presentation.md](presentation/board_presentation.md)), and plain text ([presentation/board_presentation.txt](presentation/board_presentation.txt)). The table below summarizes the nine slides and speaker notes:

| Slide Number and Title | Core Message for the Board | Nana's Spoken Summary |
| :--- | :--- | :--- |
| **Slide 1: Executive Title** | Sizing data architecture for Kloud Kart's scale (~40 gigabytes, 4,000 daily orders), not Amazon. | Commits to an affordable data plan that stops site freezes and unifies sales totals. |
| **Slide 2: Symptoms vs. Root Causes** | Website freezes and revenue arguments come from sharing one machine and lacking agreed formulas. | Explains that running Monday reports on the live store locks up customer checkouts. |
| **Slide 3: Two-Server Architecture** | Activating pre-approved Server 2 as a reporting mirror with clean analytical tables. | Shoppers use the store on Server 1; reports read from the mirror on Server 2. |
| **Slide 4: Customer Privacy (Act 843)** | Privacy cleaning at the gate and an audit log to handle both deletion and account recovery. | Complies with Ghana law within 90 days by scrubbing personal contact details before reporting. |
| **Slide 5: 99% Batch / Live Stock** | Daily 02:00 AM updates for reporting, with live checkout checks for warehouse stock. | Explains why daily reporting is 100% sufficient while physical inventory stays live. |
| **Slide 6: Two Data Hires** | Hiring a Data Engineer in Month 1 and an Analytics Engineer in Month 3; no AI or Data Scientist. | Fixes operational plumbing first before standardizing reporting; machine learning is deferred. |
| **Slide 7: Quarterly Roadmap** | Four quarters of visible outcomes, each verified by non-technical business tests. | Commits to measurable quarterly results that Nana and Finance can verify without engineers. |
| **Slide 8: Operating Assumptions** | Open disclosure of assumptions (server capacity, revenue definitions, settlement timing). | Demonstrates defensibility by stating what could not be verified in available records. |
| **Slide 9: Decision Request** | Authorize hiring the Data Engineer in Month 1 and activating the duplicate server. | Requests formal board approval to begin implementation immediately. |

---

## 4. Project Rules and Limits

Every decision in this repository respects the hard constraints set in the lab brief:

- **Two Data Hires Only:** Budget is capped at two hires this financial year (not three).
- **Live Store Must Stay Up:** The website and main database share one server; reporting must never slow down customer checkouts.
- **Second Server Pre-Approved:** A second server is already approved in the budget and serves as our isolated reporting mirror.
- **Ghana Privacy Law and Deletion Implementation Period:** Data handling must satisfy statutory erasure obligations under Ghana's Data Protection Act, 2012 (Act 843) and support deleting customer records within the active 90-day Data Protection Commission complaint resolution window, backed by permanent audit logging.
- **Stock Counts Stay Live:** Warehouse stock numbers must stay live to prevent overselling, while all other reports refresh once daily.
- **Non-Technical Sponsor:** Nana Adjei is non-technical and unavailable for follow-up questions, so every document avoids unnecessary jargon and states all assumptions openly.

---

## 5. Assumptions Made (Where Details Were Missing)

Because Nana Adjei was unavailable for interviews, this plan relies on six explicit assumptions (detailed in Section 6 of [situation_diagnosis.md](situation_diagnosis.md)):

1. **Revenue Formula Baseline:** We assume Finance counts net paid orders (excluding refunds) while Operations counts gross placed orders. Both are tracked in Quarter 1 and combined into one agreed database formula in Quarter 2.
2. **Financial Loss Estimates:** Lost sales, wasted leadership hours, and regulatory risk figures in `situation_diagnosis.md` are transparent analytical models rather than audited company ledgers.
3. **Where Nigeria Pilot Data Is Stored and Handled:** We assume Nigeria pilot orders currently write into the main Accra database (tagged by country) with personal details stripped before reporting, and that commercial expansion into Nigeria will include a simple cross-border transfer agreement under Nigerian privacy rules.
4. **Payment Gateway Settlement Cutoffs:** We assume third-party card payment processors and mobile money providers settle customer payments on standard 24-to-48-hour rolling settlement windows.
5. **Regulatory Timelines and the 90-Day Implementation Period:** Under Ghana's Data Protection Act, 2012 (Act 843), statutory data subject erasure requests carry standard operational turnaround timelines (typically within 21 calendar days). We assume the 90-day milestone represents Kloud Kart's internal Quarter 1 implementation sprint to eliminate untracked files, build the automated privacy gateway, implement the permanent deletion audit log, and formally conclude the active Data Protection Commission complaint with verified audit proof.
6. **Customer Deletion Complaint Ambiguity (Removing vs Restoring):** The brief's note of 90 days to respond to a Data Protection Commission complaint about a deleted customer's data could mean erasing personal copies across staff laptops (removing) or restoring an account deleted in error or accidentally brought back during a backup restore (restoring). We decided to solve both through pre-load data scrubbing and an immutable deletion audit log.

---

## 6. Recommended Reading Order

1. **Start with the Diagnosis:** Read [situation_diagnosis.md](situation_diagnosis.md) to see the root causes, financial costs, and assumptions.
2. **Review the Plan and Timeline:** Read [recommendation.md](recommendation.md) for the system design and staffing plan, followed by [roadmap.md](roadmap.md) for the quarterly outcomes.
3. **Check the Trade-Offs, Slides and Built Tool:** Open [decisions/](decisions/) for the five Architecture Decision Records, [customer_data_inventory_and_deletion_register.md](customer_data_inventory_and_deletion_register.md) for the built privacy/reconciliation tracker, and [presentation/](presentation/) for the board presentation deck (available in [.pptx](presentation/board_presentation.pptx), [.md](presentation/board_presentation.md), and [.txt](presentation/board_presentation.txt)).

_Note: No real database passwords, live customer records, or private personal data are stored in this repository (sample environment variables are shown in [.env.example](.env.example))._
