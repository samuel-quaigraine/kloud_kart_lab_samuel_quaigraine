# ADR-002: Use a Simple Relational Reporting Database Instead of an Expensive Data Lakehouse

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decision owner:** Nana Adjei (Head of Operations) and Kloud Kart Leadership (advised by External Data Consultant)

## Context

Following the recent funding round, board members and investors asked whether Kloud Kart should build "a modern data warehouse, or maybe a lakehouse." 

The company's total data footprint is approximately 40 gigabytes, growing by 15% to 20% annually. All company data consists exclusively of structured retail records: customer accounts, inventory items, orders, and line items. The technical budget allows for exactly two data hires for the entire year, neither of whom has experience running distributed big-data computer clusters.

## Decision

We reject building a complex data lakehouse. We establish our reporting system in a dedicated analytical schema hosted directly on the pre-approved duplicate server (read replica), storing clean, structured tables designed for standard SQL queries with zero need for a separate third database server.

## Alternatives considered

### Alternative A: Build a cloud data lakehouse using Databricks and open table formats

- **How it would work:** Raw database dumps are written to cloud storage buckets (such as Amazon S3) wrapped with file transaction layers (such as Delta Lake or Apache Iceberg). A distributed computing engine (such as Apache Spark or Databricks) runs queries across both reports and future machine learning models.
- **Why it is attractive:** It is a major industry buzzword and provides an all-in-one system for companies with petabytes of data combining text, audio, and image files.
- **Why rejected on Kloud Kart's numbers:** Lakehouses were designed for massive enterprises processing petabytes of unstructured data (such as millions of audio files and video streams). Kloud Kart has 40 gigabytes of structured retail tables. Running a distributed lakehouse requires constant cluster configuration, file compaction routines, and specialized big-data engineering skills. For two data hires managing 40 gigabytes, a lakehouse is expensive over-engineering that would consume the team's entire working hours just keeping the cluster running, with zero measurable benefit to Nana's Monday reports.

### Alternative B: Build a low-cost data lake using flat cloud file storage

- **How it would work:** Raw CSV spreadsheet files or JSON files are dumped into cloud storage buckets, and staff query the raw files directly using serverless query tools (such as Amazon Athena).
- **Why it is attractive:** Extremely cheap file storage cost and no database server software to manage.
- **Why rejected on Kloud Kart's numbers:** As I understand Act 843, when a customer requests that their personal data be deleted, Kloud Kart has a strict 90-day legal clock to locate and erase every copy. Finding and deleting an individual customer row across thousands of static files in cloud storage is technically difficult and creates a high risk of failing a legal audit. Furthermore, flat file storage does not prevent duplicate records, rapidly turning the storage into an untrusted "data swamp."

## Consequences

- **What this buys:** Immediate compatibility with standard SQL queries, zero complex cluster management, zero extra hosting fees beyond the pre-approved second server, and strict enforcement of data formats. Our second hire (the Analytics Engineer) can begin writing business models on their first day.
- **What this costs:** Kloud Kart must define table formats before loading data. Any new data fields must be planned rather than dumped randomly.
- **What it costs the client if I am wrong:** If Kloud Kart unexpectedly acquires another retail business with massive amounts of video data, migrating records to a cloud storage lakehouse would take several weeks of engineering time.
- **What would make me revisit this:** Total data size growing beyond 500 gigabytes; analytical queries taking longer than 15 minutes to run despite proper database indexing; or a genuine business requirement to process billions of raw website clickstream events.

## What this survives

This decision comfortably survives Kloud Kart's 15% to 20% annual growth for the next five years (reaching roughly 100 gigabytes). It handles all standard e-commerce reporting, financial reconciliation, and regional sales tracking across Ghana and Nigeria effortlessly.
