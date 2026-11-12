# ADR-004: Clean Private Customer Information on the Way In to Follow Ghana Data Law (Act 843)

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decision owner:** Nana Adjei (Head of Operations) and Kloud Kart Leadership (advised by External Data Consultant)

## Context

Kloud Kart stores personal records for over 300,000 customers across Ghana and Nigeria. Today, Marketing exports customer lists with no tracking of how many copies exist, allowing personal customer data to leak to unmonitored laptops. 

As I understand Act 843, Kloud Kart is legally recognized as a data controller, individuals have the legal right to request the deletion or correction of their personal data, and Kloud Kart faces an active regulatory inquiry forwarded by the Data Protection Commission regarding a customer deletion request with a strict 90-day legal response deadline.

The core architectural design rule governing this engagement is: *Every copy you create is a place a deletion request must reach.*

## Decision

We implement a two-step privacy cleaning and query loading mechanism. During nightly extraction from the duplicate mirror database, direct personal details (names, mobile telephone numbers, and street delivery addresses) are permanently removed at the gate. Customer emails are converted into irreversible anonymous codes (such as turning an email into `cust_98234`). All business transaction data (order dates, quantities, item prices, delivery regions, and cedi amounts) are loaded into a dedicated reporting schema on the second server in their original form, allowing business metrics to be modeled and calculated flexibly using standard database queries (SQL).

## Alternatives considered

### Alternative A: Dump all raw data untouched and clean it later (Pure ELT)

- **How it would work:** Every table from the operational MySQL database is copied untouched, including full customer names, telephone numbers, home delivery addresses, and payment details, and dumped straight into the reporting database. All anonymization is delayed to future queries.
- **Why it is attractive:** It is the fastest pipeline to write at first. It keeps 100% of the raw data in storage so developers can access any field in the future without re-querying the store database.
- **Why rejected on Kloud Kart's numbers:** As I understand Act 843, if raw customer contact details are duplicated across staging tables, history tables, and reporting models, complying with a Data Protection Commission deletion request within 90 days means searching and erasing records across dozens of internal tables. If even one table or backup file is missed, Kloud Kart fails the regulatory audit, incurring illustrative fines of 500,000 to 1,200,000 Ghana Cedis. With only two data hires, managing deletion cascades across multiple raw tables is an audit disaster waiting to happen.

### Alternative B: Calculate and summarize everything inside custom code before saving (Traditional ETL)

- **How it would work:** Data is extracted, and all business formulas (revenue definitions, order status checks, returns deductions) are calculated inside application code (such as Python or PHP) before saving only final summarized totals into the reporting database.
- **Why it is attractive:** The reporting database receives only clean, summarized numbers with zero raw customer records, using very little disk space.
- **Why rejected on Kloud Kart's numbers:** It is too rigid and fragile. When Operations and Finance change the formula for completed revenue next month, an engineer must rewrite the code, test it, and re-pull months of historical records from the live store database. Forcing repeated historical re-extractions places heavy load on our small single-box infrastructure and delays business reporting.

## Consequences

- **What this buys:** Complete legal defensibility under Ghana's Data Protection Act, 2012 (Act 843). Customer deletion requests only need to be executed in one single place: the primary store database. Zero personal customer records exist in the reporting database. Meanwhile, the Analytics Engineer retains full freedom to adjust revenue and order calculation queries in SQL without ever touching the live store.
- **What this costs:** The ingestion process must execute the anonymization and email hashing logic on every run. Marketing staff cannot pull raw phone numbers or email addresses directly from the reporting database.
- **What it costs the client if I am wrong:** If the Marketing team needs customer contact lists for an emergency SMS broadcast, they cannot pull it from the reporting database; they must request an authorized, logged export from the primary database administrator.
- **What would make me revisit this:** Implementation of an enterprise automated data privacy governance tool that automatically wipes records across all systems simultaneously; or an explicit legal requirement to store raw telephone numbers in internal financial audit logs.

## What this survives

This decision easily survives formal Data Protection Commission regulatory audits, investor due diligence reviews, and regional expansion into Nigeria under the Nigeria Data Protection Act.
