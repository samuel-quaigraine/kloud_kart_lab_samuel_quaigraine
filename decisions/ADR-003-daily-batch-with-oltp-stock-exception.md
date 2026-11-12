# ADR-003: Adopt a daily batch processing schedule for reporting with a single real-time exception for inventory stock counts

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decision owner:** External Data Engineering Practice

## Context

Following a board presentation where an investor saw a live streaming dashboard at another portfolio company, Kloud Kart's leadership was urged to implement "real-time analytics." 

However, Kloud Kart operates with a strict budget of two data hires who must also ensure system reliability. Real-time stream processing requires continuous 24-hour infrastructure, complex event deduplication, and an intensive on-call monitoring burden. Furthermore, the operational brief establishes a critical business constraint: *"Stock counts cannot go stale (that is how the company oversells); everything else can refresh daily."*

## Decision

We establish an automated 24-hour daily batch processing cadence (running at 02:00 AM) for 99% of analytical reporting, financial ledgers, and marketing metrics. We designate warehouse physical stock counts as the single, strictly transactional real-time exception, maintained and queried directly on the primary live database.

## Alternatives considered

### Alternative A: Build an end-to-end real-time streaming pipeline using Apache Kafka and stream processors

- **How it would work:** Every storefront interaction, shopping cart change, order update, and inventory movement is published immediately as an event stream into a message broker (such as Apache Kafka or Amazon Kinesis). A continuous stream processing engine (such as Apache Flink) computes live running totals and feeds real-time updating dashboards.
- **Why it is attractive:** It provides sub-second reporting dashboards and directly satisfies the board's interest in real-time technological capabilities.
- **Why rejected:** We apply the operational decision test: *"What business decision changes if this number is 10 seconds old instead of 24 hours old?"* Strategic marketing budget allocation, weekly category review, and monthly revenue reconciliation do not change minute by minute. A 24-hour daily refresh is completely sufficient for leadership decision-making. Operating continuous streaming infrastructure creates significant cost for idle capacity and introduces complex failure modes (such as out-of-order events, network partitions, and duplicate message delivery) that would overwhelm a two-person engineering team.

### Alternative B: Pure 100% batch processing with zero real-time exceptions (including inventory stock)

- **How it would work:** All data without exception—including inventory stock levels—is captured, transformed, and updated exclusively through the nightly 02:00 AM batch pipeline.
- **Why it is attractive:** Maximizes architectural simplicity by having only one unified processing mechanism across the entire business.
- **Why rejected:** It violates the core business requirement. If physical inventory counts are refreshed only once every 24 hours, the website displays outdated availability throughout the shopping day. When multiple shoppers purchase fast-moving items simultaneously, Kloud Kart oversells goods that do not exist on the warehouse shelf. This forces customer service call interventions, refund processing fees, bank chargebacks, and unquantifiable customer goodwill erosion.

## Consequences

- **What this buys:** Predictable, easily debugged, and reproducible batch pipelines that can be re-run safely if an error occurs. Zero on-call streaming alerts waking engineers up in the middle of the night. Flawless live inventory accuracy that permanently eliminates overselling cancellations.
- **What this costs:** Departmental managers must accept that operational reporting dashboards reflect data up to the close of business yesterday (up to 24 hours old).
- **What it costs the client if I am wrong:** If the Marketing department launches high-velocity flash sales that require intraday ad spend adjustments every 30 minutes, they will lack hourly conversion feedback, resulting in potential ad budget inefficiency during single-day sales events.
- **What would make me revisit this:** Daily order volumes scaling beyond 25,000 orders per day; automated dynamic pricing algorithms requiring live demand signals; or an automated warehouse robotics system requiring millisecond routing updates.

## What this survives

This decision comfortably survives growth up to 10,000 orders per day across Ghana and Nigeria. It protects storefront checkout integrity while keeping operating costs and engineering overhead strictly bounded.

