# Kloud Kart: 12-Month Data Plan & System Design

> **Project:** AmaliTech Data Engineering Foundations (DE01) Lab  
> **Client:** Nana Adjei, Head of Operations, Kloud Kart  
> **Author:** Samuel Quaigraine  
> **Status:** Complete & Aligned to Lab Brief and Rubric

---

## 1. Overview: The Problem & Our Plan

Kloud Kart is a three-year-old online store in Accra, Ghana, shipping about **4,000 orders per day** with a **40 GB MySQL database** and a new expansion pilot in Nigeria.

Right now, the live PHP website and the MySQL database share a **single server**, maintained by **one developer**. That setup causes three serious business problems:

1. **Monday Morning Site Slowdowns:** Running heavy weekly reports directly on the live database slows down customer checkouts during peak morning shopping hours.
2. **Conflicting Revenue Numbers:** Operations and Finance calculate weekly revenue in separate spreadsheets with different formulas, so their totals never match.
3. **Uncontrolled Customer Data Copies:** Staff across Operations, Finance, and Marketing routinely export customer lists (estimated at ~300,000 records) into untracked spreadsheets on personal laptops, creating compliance risk (as I understand Ghana's Data Protection Act, 2012 / Act 843) while Kloud Kart faces an active **Data Protection Commission (DPC) deletion complaint** with a 90-day implementation period to prove full erasure.

### What We Decided to Build

Instead of buying expensive cloud platforms, we use the pre-approved second server as a **read-only mirror copy** of the live database (`ADR-001`) and store clean reporting tables inside a dedicated area on that same second server (`ADR-002`). We strip out private customer contact details before loading data into the reporting layer while keeping order numbers flexible for SQL calculations and logging every deletion in a permanent audit log (`ADR-004`), keep live warehouse stock checks on the main store database while refreshing reports nightly (`ADR-003`), and hire a **Data Engineer first (Month 1)** followed by an **Analytics Engineer (Month 3)** (`ADR-005`).

---

## 2. Guide to the Files in This Repository

| File                                                                                                                                    | What It Contains                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Rubric Criterion            |
| :-------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------- |
| [situation_diagnosis.md](situation_diagnosis.md)                                                                                        | Separates surface symptoms from root causes, estimates financial losses, ranks risks for the board, lists discovery questions, and states all assumptions.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | **Analyze (25%)**           |
| [recommendation.md](recommendation.md)                                                                                                  | Two-page system design sized for 40 GB, rough costs, first-90-day goals for both hires, and direct answers to hard investor questions.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | **Evaluate (25%)**          |
| [roadmap.md](roadmap.md)                                                                                                                | One-page, 12-month quarterly plan written as plain business outcomes Nana Adjei can verify herself without asking an engineer.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | **Create (25%)**            |
| [decisions/](decisions/) (5 ADRs)                                                                                                       | Five Architecture Decision Records comparing real alternatives, pricing the cost of mistakes, and defining when to revisit each choice:<br>- [ADR-001](decisions/ADR-001-reporting-reads-from-read-replica.md): Run reports on a duplicate server (read replica).<br>- [ADR-002](decisions/ADR-002-relational-warehouse-over-lakehouse.md): Use simple SQL tables instead of a data lakehouse.<br>- [ADR-003](decisions/ADR-003-daily-batch-with-oltp-stock-exception.md): Update reports nightly, but keep warehouse stock live.<br>- [ADR-004](decisions/ADR-004-hybrid-elt-with-pii-masking-under-act-843.md): Remove private customer details before loading.<br>- [ADR-005](decisions/ADR-005-hiring-data-engineer-then-analytics-engineer.md): Hire a Data Engineer first, then an Analytics Engineer. | **Evaluate / Create (25%)** |
| [presentation/board_presentation.md](presentation/board_presentation.md) | Short, jargon-free board presentation with speaker notes for Nana Adjei, including a clear list of what could not be verified (also available in plain text for PowerPoint authoring: [board_presentation.txt](presentation/board_presentation.txt)). | **Evaluate / Create (25%)** |
| [improvement.md](improvement.md) & [customer_data_inventory_and_deletion_register.md](customer_data_inventory_and_deletion_register.md) | Extra deliverable built beyond the brief: tracks where customer copies live across Operations, Finance, and Marketing, maintains the permanent deletion audit log and DPC response register, and sets a Monday revenue sign-off checklist. | **Create (25%)** |
| [erd_and_architecture.md](erd_and_architecture.md)                                                                                      | System diagrams showing how data flows from the live store to the reporting server and how the clean reporting tables connect.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Supporting Visuals          |

---

## 3. Project Rules & Limits

Every decision in this repository respects the hard constraints set in the lab brief:

- **Two Data Hires Only:** Budget is capped at two hires this financial year (not three).
- **Live Store Must Stay Up:** The website and main database share one server; reporting must never slow down customer checkouts.
- **Second Server Pre-Approved:** A second server is already approved in the budget and serves as our isolated reporting mirror.
- **Ghana Privacy Law & Deletion Implementation Period:** Data handling must be defensible (as I understand Act 843) and support deleting a customer's records within the active 90-day DPC complaint resolution window, backed by permanent audit logging.
- **Stock Counts Stay Live:** Warehouse stock numbers must stay live to prevent overselling, while all other reports refresh once daily.
- **Non-Technical Sponsor:** Nana Adjei is non-technical and unavailable for follow-up questions, so every document avoids unnecessary jargon and states all assumptions openly.

---

## 4. Assumptions Made (Where Details Were Missing)

Because Nana Adjei was unavailable for interviews, this plan relies on five explicit assumptions (detailed in Section 6 of [situation_diagnosis.md](situation_diagnosis.md)):

1. **Revenue Formula Baseline:** We assume Finance counts net paid orders (excluding refunds) while Operations counts gross placed orders. Both are tracked in Q1 and combined into one agreed SQL formula in Q2.
2. **Financial Loss Estimates:** Lost sales, wasted leadership hours, and regulatory risk figures in `situation_diagnosis.md` are transparent analytical models rather than audited company ledgers.
3. **Where Nigeria Pilot Data Is Stored:** We assume Nigeria pilot orders currently write into the main Accra database (tagged by country) rather than a separate server in Nigeria.
4. **Payment Gateway Settlement Cutoffs:** We assume third-party card payment processors and mobile money providers settle customer payments on standard 24-to-48-hour rolling settlement windows.
5. **Regulatory Timelines and the 90-Day Implementation Period:** Under Ghana's Data Protection Act, 2012 (Act 843), statutory data subject erasure requests carry standard operational turnaround timelines (typically within 21 calendar days). We assume the 90-day milestone represents Kloud Kart's internal Quarter 1 implementation sprint to eliminate untracked files, build the automated privacy gateway, implement the permanent deletion audit log, and formally conclude the active Data Protection Commission complaint with verified audit proof.

---

## 5. Recommended Reading Order

1. **Start with the Diagnosis:** Read [situation_diagnosis.md](situation_diagnosis.md) to see the root causes, financial costs, and assumptions.
2. **Review the Plan & Timeline:** Read [recommendation.md](recommendation.md) for the system design and staffing plan, followed by [roadmap.md](roadmap.md) for the quarterly outcomes.
3. **Check the Trade-Offs, Slides & Built Tool:** Open [decisions/](decisions/) for the five ADRs, [customer_data_inventory_and_deletion_register.md](customer_data_inventory_and_deletion_register.md) for the built privacy/reconciliation tracker, and [presentation/board_presentation.md](presentation/board_presentation.md) (or [presentation/board_presentation.txt](presentation/board_presentation.txt)) for the board deck.

_Note: No real database passwords, live customer records, or private personal data are stored in this repository (sample environment variables are shown in [.env.example](.env.example))._
