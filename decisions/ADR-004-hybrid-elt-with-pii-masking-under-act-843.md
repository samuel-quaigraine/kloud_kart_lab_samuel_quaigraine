# ADR-004: Implement two-step privacy sanitization and query loading under Ghana's Data Protection Act

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decision owner:** External Data Engineering Practice

## Context

Kloud Kart processes personal information for over 300,000 customers across Ghana and Nigeria. Currently, customer records are exported in unencrypted spreadsheets across departmental laptops. 

Under Ghana's Data Protection Act, 2012 (Act 843), Kloud Kart is legally classified as a data controller. Section 33 of Act 843 grants individuals the statutory right to request the deletion or correction of their personal data. Kloud Kart already faces an active regulatory complaint with the Data Protection Commission regarding a deleted customer's record, establishing a strict 90-day response window. 

The core architectural design rule governing this engagement is: *"Every copy you create is a place a deletion request must reach."*

## Decision

We implement a two-step privacy sanitization and query loading mechanism. During nightly extraction from the duplicate database server, direct customer identifiers (names, mobile telephone numbers, and street delivery addresses) are stripped out, and customer email addresses are converted into one-way anonymous identification codes (such as `cust_98234`). All business transaction facts (quantities, prices, dates, delivery regions, and order totals) are loaded into the central reporting database in their original form, allowing business metrics to be modeled and calculated flexibly using database queries.

## Alternatives considered

### Alternative A: Pure modern extraction and loading without upfront sanitization (Pure ELT)

- **How it would work:** All tables from the operational MySQL database are extracted completely untouched—including customer names, telephone numbers, home delivery addresses, and payment details—and dumped directly into the central reporting database. All cleaning and anonymization is deferred to subsequent database queries.
- **Why it is attractive:** It is the fastest pipeline to write initially. It preserves 100% of the raw data indefinitely, allowing future developers to reconstruct any missing field without re-querying the operational database.
- **Why rejected:** It directly violates the Act 843 data minimization principle (Section 19) and multiplies regulatory risk. If raw customer contact details are duplicated across staging tables, history logs, and analytical data marts, complying with a formal Data Protection Commission deletion request within 90 days requires auditing and wiping records across dozens of internal tables. If a single table or backup is missed, Kloud Kart legally fails a regulatory audit, incurring substantial financial penalties and reputational sanctions.

### Alternative B: Traditional rigid pipeline transformation (Traditional ETL)

- **How it would work:** Data is extracted, and all business calculations (revenue definitions, customer grouping, returns processing) are executed within procedural application code (Python or PHP) before loading only finalized aggregate summaries into the reporting database.
- **Why it is attractive:** The reporting database receives only clean, summarized numbers with zero raw customer records, minimizing storage requirements.
- **Why rejected:** It is excessively rigid and fragile. When Operations and Finance adjust the business definition of completed revenue, an engineer must rewrite the pipeline code, redeploy the software, and re-extract historical records from the operational database. Forcing repeated historical re-extractions places unnecessary load on database infrastructure and delays business reporting.

## Consequences

- **What this buys:** Robust legal defensibility under Ghana's Data Protection Act. Customer deletion requests only need to be executed on the primary operational database, because personal contact data never enters the reporting layer. Analysts and leadership retain complete flexibility to adjust revenue and order calculation queries in the reporting database without touching the live shop.
- **What this costs:** The initial ingestion script must maintain and execute the anonymization and email hashing logic. Marketing analysts cannot perform direct phone or email outreach campaigns directly from the reporting database.
- **What it costs the client if I am wrong:** If the Marketing department requires individualized customer contact lists for urgent seasonal SMS campaigns, they must request an authorized, audited export from the primary database administrator rather than querying the reporting database directly.
- **What would make me revisit this:** Implementation of a formal enterprise customer identity governance platform with automated deletion propagation; or legal requirements requiring customer telephone numbers to be stored in analytical audit logs.

## What this survives

This decision survives formal Data Protection Commission regulatory audits, investor due diligence reviews, and expansion into additional African jurisdictions (such as Nigeria under the Nigeria Data Protection Act).

