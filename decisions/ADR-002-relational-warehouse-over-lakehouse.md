# ADR-002: Deploy a standard relational reporting database rather than a distributed data lakehouse

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decision owner:** External Data Engineering Practice

## Context

Following the recent funding round, board members and investors asked whether Kloud Kart should build "a data warehouse, or maybe a lakehouse." The company's total data footprint is approximately 40 gigabytes, growing by 15% to 20% annually. All data consists exclusively of structured, relational business records: customer accounts, inventory catalog items, orders, and order line items. The engineering team is limited to two data hires for the entire financial year, neither of whom has operated distributed big data clusters.

## Decision

We reject building a distributed data lakehouse. We establish our analytical reporting layer on a standard, managed relational database (such as PostgreSQL or a dedicated analytical reporting schema) that stores clean, structured tables optimized for SQL queries.

## Alternatives considered

### Alternative A: Build a cloud data lakehouse using Databricks and open table formats (Delta Lake or Apache Iceberg)

- **How it would work:** Raw database dumps are written to cloud object storage (such as Amazon S3) wrapped with metadata transaction layers (Delta Lake or Apache Iceberg). A distributed computing engine (such as Apache Spark or Databricks) executes queries across both business reports and future machine learning models.
- **Why it is attractive:** It represents the leading industry buzzword and promises a single platform that unifies traditional business intelligence with future machine learning experiments.
- **Why rejected:** Lakehouses were specifically invented to solve a problem Kloud Kart does not have: managing petabytes of messy, unstructured data (such as video recordings, customer service audio logs, and high-frequency sensor streams) alongside tabular data. Operating a distributed lakehouse requires extensive cluster tuning, complex file compaction routines, and specialized distributed computing skills. For a 40-gigabyte structured database managed by two engineers, a lakehouse is extreme over-engineering that would consume the team's entire capacity in maintenance overhead with zero measurable business benefit.

### Alternative B: Build a low-cost data lake using flat cloud object storage (Amazon S3 or Google Cloud Storage)

- **How it would work:** Raw CSV or JSON data extracts are dumped into cloud storage buckets, and analysts run queries directly over the raw files using serverless query tools (such as Amazon Athena).
- **Why it is attractive:** Extremely inexpensive storage cost and zero database servers to manage.
- **Why rejected:** Without rigid schema enforcement on write, data lakes rapidly degenerate into "data swamps" where multiple outdated versions of customer lists coexist. Crucially, under Section 33 of Ghana's Data Protection Act, 2012 (Act 843), when a customer requests data deletion, locating and purging their specific records across thousands of flat files in cloud storage is technically complex and prone to audit failure. Flat files do not support reliable record-level updates and transactional consistency.

## Consequences

- **What this buys:** Immediate compatibility with standard SQL, zero distributed cluster maintenance, predictable low operating costs (under 800 Ghana Cedis per month), and rigid enforcement of data types and relational integrity. The Analytics Engineer can begin modeling business revenue on day one using standard tools.
- **What this costs:** Kloud Kart must define table schemas before loading data. Any new source data requires schema modeling rather than ad-hoc dumping.
- **What it costs the client if I am wrong:** If Kloud Kart unexpectedly acquires another company with massive unstructured data or pivots into an image-heavy media platform, migrating data to an object-based lakehouse would cost several weeks of engineering transition time.
- **What would make me revisit this:** Total data volume exceeding 500 gigabytes; analytical query execution times consistently exceeding acceptable reporting windows (over ten minutes) despite proper indexing; or a genuine business requirement to process vast unstructured clickstreams.

## What this survives

This architecture comfortably survives Kloud Kart's steady 15% to 20% annual growth for the next five years (reaching approximately 100 gigabytes). It handles all standard e-commerce reporting, financial reconciliation, and regional market analysis for Ghana and Nigeria effortlessly.

