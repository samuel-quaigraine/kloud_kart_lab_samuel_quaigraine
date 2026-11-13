# ADR-002: Use a Simple Relational Reporting Database Instead of an Expensive Data Lakehouse

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decision owner:** Nana Adjei (Head of Operations) and Kloud Kart Leadership (advised by External Data Consultant)

## Context

Following the recent funding round, board members and investors asked whether Kloud Kart should build "a modern data warehouse, or maybe a lakehouse."

The company's total data footprint is approximately 40 gigabytes, growing by 15% to 20% annually. All company data consists of structured retail records: customer accounts, inventory, and orders. With budget for only two data hires all year, the team cannot take on the heavy daily maintenance of a distributed cluster while also ensuring the shared database never slows down or crashes the live store.

## Decision

We reject building a complex data lakehouse. We establish our reporting system in a dedicated analytical schema hosted directly on the pre-approved duplicate server (read replica), storing clean, structured tables designed for standard Structured Query Language (SQL) queries with zero need for a separate third database server. This relational reporting schema cleanly separates analytics by territory using country-dimension attributes and SQL views, allowing the business to isolate early Nigeria pilot numbers from Ghana's core revenue without needing a multi-region cloud data infrastructure.

## Alternatives considered

### Alternative A: Build a cloud data lakehouse

- **How it would work:** Raw database copies are saved into cloud object storage using open table formats, and a distributed computing engine (such as Apache Spark) runs both daily business reports and future machine learning models from that storage.
- **Why it is attractive:** It keeps all company data in an open format without locking Kloud Kart into a single database vendor, and it supports future machine learning models as the business grows.
- **Why rejected:** Lakehouses were designed for massive enterprises processing petabytes of unstructured data (such as millions of audio files and video streams). Kloud Kart has 40 gigabytes of structured retail tables. Running a distributed lakehouse requires constant cluster configuration, file compaction routines, and specialized big-data engineering skills. For two data hires managing 40 gigabytes, a lakehouse is expensive over-engineering that would consume the team's entire working hours just keeping the cluster running, with zero measurable benefit to Nana's Monday reports.

### Alternative B: Build a low-cost data lake using flat cloud file storage

- **How it would work:** Raw CSV exports from MySQL are saved directly into low-cost cloud file storage (such as Amazon S3), and staff query those static files directly using a serverless query tool(such as Amazon Athena).
- **Why it is attractive:** File storage is very cheap, and there is no database server software to install or maintain. The team can dump raw files quickly and expand storage as the company grows.

- **Why rejected:** As I understand Act 843, when a customer requests that their personal data be deleted, Kloud Kart has a strict 90-day legal clock to locate and erase every copy. Finding and deleting an individual customer row across thousands of static files in cloud storage is technically difficult and creates a high risk of failing a legal audit. Furthermore, flat file storage does not prevent duplicate records, rapidly turning the storage into an untrusted "data swamp."

## Consequences

- **What this buys:** Immediate compatibility with standard SQL queries, zero complex cluster management, zero extra hosting fees beyond the pre-approved second server, and strict enforcement of data formats. Our second hire (the Analytics Engineer) can begin writing business models on their first day, including dedicated views that keep early Nigeria pilot metrics completely separate from core Ghana sales.
- **What this costs:** Kloud Kart must define table formats before loading data. Any new data fields must be planned rather than dumped randomly.
- **What it costs the client if I am wrong:** If Kloud Kart unexpectedly acquires another business with massive amounts of video data, migrating records to a cloud storage lakehouse would take several weeks of engineering time.
- **What would make me revisit this:** Total data size growing beyond 500 gigabytes; analytical queries taking longer than 15 minutes to run despite proper database indexing; or a genuine business requirement to process billions of raw website clickstream events.

## What this survives

This decision comfortably survives Kloud Kart's 15% to 20% annual growth for the next five years (reaching roughly 100 gigabytes). It handles all standard e-commerce reporting, financial reconciliation, and regional sales tracking across Ghana and Nigeria effortlessly.
