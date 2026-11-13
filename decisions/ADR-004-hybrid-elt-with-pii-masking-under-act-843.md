# ADR-004: Clean Private Customer Information on the Way In to Follow Ghana Data Law (Act 843)

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decision owner:** Nana Adjei (Head of Operations) and Kloud Kart Leadership (advised by External Data Consultant)

## Context

Kloud Kart stores customer records for over 300,000 online shoppers across Ghana and Nigeria. Today, staff across Operations (Nana Adjei), Finance, and Marketing routinely export customer lists (including Marketing's ~300,000-person list) into uncounted spreadsheets on personal laptops, allowing personal customer records to spread outside database security controls.

As I understand Ghana's Data Protection Act, 2012 (Act 843), Kloud Kart is legally recognized as a data controller. Individuals have the statutory right to request the deletion or correction of their personal data (with standard turnaround guidelines requiring action within 21 calendar days). Kloud Kart currently faces an active regulatory complaint forwarded by Ghana's Data Protection Commission (DPC) regarding a customer deletion request, and company leadership has established a 90-day internal implementation period to prove that all copies of that customer's personal data have been completely erased and establish repeatable ongoing compliance.

The core architectural rule governing this engagement is: _Every copy you create is a place a deletion request must reach._

To build an automated reporting platform on our pre-approved duplicate server, we must decide how to extract and load data from our live store. The engineering dilemma is choosing between two standard data pipeline patterns:

1. **Extract, Transform, Load (ETL):** Transforming data and stripping personal details inside custom programming code before saving it into the reporting database.
2. **Extract, Load, Transform (ELT):** Loading raw operational data into the reporting database first, and transforming numbers later using database queries.

## Decision

We adopt a **hybrid data loading method** (combining pre-load privacy masking with post-load query transformation). This hybrid approach bridges Extract, Transform, Load (ETL) and Extract, Load, Transform (ELT) into two distinct, deliberate stages:

1. **Stage 1 (Pre-Load Privacy Transformation / The Gate):** During the daily data extraction from the duplicate mirror database, an automated ingestion script permanently strips out all direct Personally Identifiable Information (PII), specifically customer full names, mobile telephone numbers, and residential delivery addresses, before the data ever enters the reporting database. Customer email addresses are converted into irreversible, one-way anonymous reference codes (such as turning an email into `cust_98234`).
2. **Stage 2 (Post-Load Business Transformation / Flexible Modeling):** All core business transaction records (order timestamps, item quantities, product prices, delivery regions, and order amounts in Ghana Cedis) are loaded into the dedicated reporting database untouched. Business metrics (such as confirmed revenue definitions and order fulfillment statuses) are modeled flexibly after loading using standard Structured Query Language (SQL) database queries.
3. **Stage 3 (Permanent Deletion Audit Logging and Targeted Recovery):** Whenever a customer deletion request is processed, an immutable entry is logged in a permanent deletion audit table (recording the masked customer ID, timestamp, and deletion reason, without storing personal contact details). This permanent audit log provides regulatory proof for the Data Protection Commission (DPC), enables automated post-restore deletion re-application, and permits targeted recovery of anonymized transaction history if an account was ever flagged in error without restoring personal data.

This hybrid method gives Kloud Kart the legal safety of privacy cleaning at the gate without sacrificing the analytical flexibility of database modeling.

## Alternatives considered

### Alternative A: Dump all raw customer data untouched and clean it later (Pure Extract, Load, Transform / ELT)

- **How it would work:** Every table from the operational MySQL database is copied 100% untouched into the reporting database, including raw Personally Identifiable Information (PII) such as full customer names, telephone numbers, delivery addresses, and payment details. All anonymization and masking are delayed to downstream database queries.
- **Why it is attractive:** It is the fastest pipeline for an engineer to build initially. It keeps every single piece of customer data in reporting storage so developers can access any field in the future without touching the live store database.
- **Why rejected:** As I understand Act 843, if raw customer contact details are duplicated across reporting tables, history logs, and backup files, complying with a Data Protection Commission (DPC) deletion request within 90 days requires searching, locating, and erasing records across dozens of internal tables. If even one table or backup copy is missed, Kloud Kart fails the regulatory audit, exposing the company to regulatory sanctions, legal and audit costs, and investor due-diligence friction estimated at 500,000 to 1,200,000 Ghana Cedis. With only two data hires, managing deletion cascades across multiple raw tables is a severe legal risk.

### Alternative B: Calculate and summarize everything inside custom code before saving (Traditional Extract, Transform, Load / ETL)

- **How it would work:** Data is extracted, and all business formulas (such as revenue definitions, order status checks, and customer retention metrics) are calculated entirely inside custom application code (such as Python scripts) before saving only final aggregated summary numbers into the reporting database, discarding all individual transaction rows.
- **Why it is attractive:** The reporting database contains zero individual customer rows and only high-level summary totals, taking up almost no disk space and eliminating customer privacy risks completely.
- **Why rejected:** It is far too rigid and fragile for a growing retail business. When Operations and Finance refine the formula for confirmed revenue next month, an engineer must rewrite the program code, test it, and re-pull months of historical records from the live store database. Forcing repeated historical re-extractions places heavy load on our small single-box infrastructure and delays business reporting.

## Consequences

- **What this buys:** Complete legal defensibility under Ghana's Data Protection Act, 2012 (Act 843). When a customer requests deletion, Kloud Kart only needs to erase the record in one single place: the primary store database, with disaster recovery procedures automatically re-applying deletions to restored backups from the permanent deletion audit log so personal records stay permanently erased. Zero Personally Identifiable Information (PII) exists in the reporting database. In the event an account is flagged for deletion in error, the audit log allows targeted operational recovery of the anonymized order history while keeping private details erased. Meanwhile, because underlying transaction rows are preserved, our Analytics Engineer retains full freedom to adjust revenue and order calculation queries in Structured Query Language (SQL) without ever touching the live store.
- **What this costs:** The daily automated ingestion script must run the privacy scrubbing and email hashing routine on every batch run. Staff across departments cannot look up customer telephone numbers or plain email addresses from the reporting database. In addition, because older system backups contain historical snapshots of deleted records, all disaster recovery database restoration runbooks must include an automated step that immediately re-applies the customer deletion register so restored backups never accidentally restore erased personal details into the live database.
- **What it costs the client if I am wrong:** If department leads genuinely need raw customer contact lists for authorized communications, they cannot pull them from the reporting database; they must request an authorized, logged export directly from the primary database administrator.
- **What would make me revisit this:** Implementation of an enterprise automated data privacy governance tool that automatically wipes records across all systems simultaneously; or an explicit legal requirement to store raw telephone numbers in internal financial audit logs.

## What this survives

This decision easily survives formal Data Protection Commission (DPC) regulatory audits, investor due-diligence reviews, and regional expansion into Nigeria, while leaving room to add country-specific controls as our legal counsel advises under Nigeria's data protection rules.
