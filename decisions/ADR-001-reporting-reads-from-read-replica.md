# ADR-001: Reporting queries read from a read replica, not from the production database

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decision owner:** External Data Engineering Practice

## Context

Kloud Kart operates customer accounts, order processing, and inventory on a single MySQL database instance hosted on the exact same physical server as the live website. Every Monday morning, Nana Adjei runs heavy reporting queries and exports large spreadsheet files containing hundreds of thousands of rows. 

Twice last month, this analytical export consumed available memory and processor capacity, slowing website checkout page loads to a crawl while shoppers were actively attempting to purchase items. A second database server machine has already been pre-approved in the company budget. The technical team consists of one developer, and the engineering plan must be operable by a two-person data team.

## Decision

We deploy the pre-approved second server as an automated, read-only mirror (read replica) of the primary MySQL database. All operational reporting queries, exports, and analytics workloads are redirected to this replica, leaving the primary database dedicated exclusively to live storefront transactions and immediate inventory stock checks.

## Alternatives considered

### Alternative A: Keep one database and throttle exports to run off-peak at 02:00 AM

- **How it would work:** The company remains on a single physical machine. Nana's export queries are rescheduled to run automatically at 02:00 AM on Monday morning with strict processor and memory throttling applied.
- **Why it is attractive:** Zero added infrastructure cost, no second server to manage, and no replication software or synchronization to monitor. It could be put in place immediately by the existing PHP developer.
- **Why rejected:** Off-peak hours are only quiet while Kloud Kart operates solely in Ghana. The active pilot expansion into Nigeria and future regional expansion will expand order volume across different time zones. Furthermore, it treats the symptom rather than the root cause; analytical queries remain physically coupled to the customer cash register, leaving the storefront permanently vulnerable to accidental heavy queries during daytime business hours.

### Alternative B: Purchase a managed cloud data warehouse immediately

- **How it would work:** Kloud Kart signs an enterprise contract with a cloud data warehouse provider (such as Snowflake or Google BigQuery). Data is transferred nightly out of MySQL into the cloud warehouse, and all internal reports are pointed at the cloud warehouse.
- **Why it is attractive:** It completely isolates reporting from the live shop and offers elastic computing capacity that scales automatically. The company developer already requested this solution.
- **Why rejected:** It introduces an unbudgeted, recurring consumption fee that caused the Finance department to flinch. Kloud Kart only possesses 40 gigabytes of data. Paying per-second compute fees for 40 gigabytes of structured data is financially irresponsible for an early-stage company with a two-person data team. Setting up cloud pipelines and data models would take months, whereas deploying the pre-approved replica stops the website crashes immediately.

## Consequences

- **What this buys:** The live e-commerce website is completely isolated from analytical reporting queries. Heavy Monday morning exports can no longer degrade storefront performance or cause customer checkout failures. Operations and Finance query the same underlying transactional data.
- **What this costs:** Kloud Kart must pay the monthly server hosting fee for the second machine (already budgeted). The new Data Engineer must monitor replication synchronization to ensure the duplicate database does not fall behind the primary database.
- **What it costs the client if I am wrong:** If replication synchronization lags significantly during peak order periods, analytical reports will reflect delayed numbers. Most critically, if an engineer mistakenly configures the website to read live inventory stock counts from the replica while replication is lagging, the store will display stale stock counts and oversell products, resulting in customer service complaints, refunds, and reputational harm.
- **What would make me revisit this:** Replication lag regularly exceeding sixty seconds under high shopping load; a requirement to store years of historical analytical records that exceed the local hard drive storage capacity of the second server; or analytical joins becoming too complex for a standard relational database to complete within acceptable time limits.

## What this survives

This architectural decision comfortably survives order volumes doubling to 8,000 orders per day and the Nigeria pilot scaling to match Ghana sales volume. The storefront transaction pathway remains completely unchanged and protected. It does not survive complex real-time distributed analytics across multiple international fulfillment hubs, which would justify a dedicated analytical warehouse in year two.

