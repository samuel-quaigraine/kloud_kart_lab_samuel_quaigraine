# ADR-001: Use a Duplicate Database Server (Mirror) for Reports to Stop Website Slowdowns

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decision owner:** Nana Adjei (Head of Operations) and Kloud Kart Leadership (advised by External Data Consultant)

## Context

Kloud Kart manages customer accounts, order checkout, and inventory on a single MySQL database hosted on the exact same physical computer as the live PHP website. Every Monday morning, Nana Adjei runs heavy reporting queries and exports large spreadsheet files containing hundreds of thousands of rows.

Twice last month, Monday reporting exports overloaded our shared server and slowed down the live website while shoppers were trying to buy. A second server (read replica) is already pre-approved in our budget. Right now, we only have one PHP/MySQL developer, so any new data system must be simple enough for our approved two-person data team to run.

## Decision

We deploy the pre-approved second server as an automated duplicate database mirror (often called a read replica). All reporting queries, spreadsheet exports, and analytics workloads are redirected to this duplicate mirror server, leaving the primary database dedicated exclusively to live storefront checkouts and immediate inventory reservations.

## Alternatives considered

### Alternative A: Keep a single database and run reporting queries at 02:00 AM

- **How it would work:** Kloud Kart stays on a single physical machine. Nana's export queries are rescheduled to run automatically at 02:00 AM on Monday morning with strict limits on processor usage.
- **Why it is attractive:** Zero extra hosting cost, no second machine to configure, and no database replication links to monitor. It could be scheduled immediately by the existing PHP developer.
- **Why rejected:** Kloud Kart ships about 4,000 orders per day and is actively expanding into Nigeria, where peak shopping hours and late-night buying habits differ from Ghana. Relying on an off-peak window on a single shared box leaves customer checkouts permanently exposed. When an unplanned daytime query is run, the live checkout process freezes again, losing sales. Treating the symptom on a shared box is unacceptable when a second server is already pre-approved in the budget.

### Alternative B: Purchase an enterprise cloud data warehouse immediately

- **How it would work:** Kloud Kart subscribes to a managed cloud data warehouse (such as Snowflake or Google BigQuery), copies data out of MySQL on a daily schedule, and points all staff dashboards there.

- **Why it is attractive:** It completely isolates reporting from the live shop and automatically scales processor power during heavy queries. The sole developer requested this tool.
- **Why rejected:** Kloud Kart only has 40 gigabytes of structured data, so paying monthly cloud platform fees and usage bills is unnecessary overhead. More importantly, an external cloud warehouse adds daily operational drag on our two-person team, who would have to spend their time managing cloud security, billing, and sync pipelines while also keeping the live shop running. Setting up a new cloud environment would also delay relief, whereas turning on the pre-approved duplicate server stops website slowdowns immediately.

## Consequences

- **What this buys:** The live store is completely protected from reporting queries. Heavy Monday morning exports cannot slow down customer checkout or cause dropped carts. Operations and Finance query the same underlying transaction records.
- **What this costs:** Kloud Kart pays the monthly hosting fee for the second server (already approved in the budget). The new Data Engineer must monitor the replication link to make sure the mirror does not fall behind the primary database.
- **What it costs the client if I am wrong:** If the mirror lags behind the live database during peak shopping hours, morning reports will show slightly delayed numbers. Most critically, if an engineer mistakenly configures the website to check live inventory stock counts from the mirror while it is lagging, the store will display out-of-date stock counts and oversell products, causing customer complaints and refund processing costs.
- **What would make me revisit this:** Replication lag regularly exceeding 60 seconds under high order volume; total data size growing beyond the hard drive capacity of the second server; or complex reporting queries taking more than 30 minutes to finish on a relational database.

## What this survives

This decision comfortably survives order volumes doubling to 8,000 orders per day and the Nigeria pilot growing to match Ghana order volumes. The storefront transaction path remains completely protected. It does not survive complex real-time analytics across multiple international fulfillment hubs, which would justify a dedicated analytical warehouse in year two.
