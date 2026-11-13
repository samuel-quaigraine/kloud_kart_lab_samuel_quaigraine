# ADR-003: Update Reports Once Every Night in Batch, but Keep Live Warehouse Stock Real-Time

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decision owner:** Nana Adjei (Head of Operations) and Kloud Kart Leadership (advised by External Data Consultant)

## Context

Following a board meeting where an investor mentioned seeing live updating screens at another company, Kloud Kart's leadership was encouraged to build "real-time analytics."

However, Kloud Kart operates with a strict budget of two data hires who must keep systems reliable without burning out. Real-time streaming requires servers running 24 hours a day, complex message tracking, and constant on-call alerts. Furthermore, our business rules establish one critical requirement: _"Stock counts cannot go stale (that is how the company oversells); everything else can refresh daily."_

## Decision

We establish an automated daily batch schedule (running at 02:00 AM) for 99% of company reports, financial reconciliation ledgers, and marketing dashboards. We set warehouse physical stock counts as the single, strict real-time exception, checked live on the primary store database during customer checkout.

In addition, to prevent warehouse shelf counts and online catalog numbers from drifting apart, the daily batch extraction routine executes an automated daily stock drift check comparing recorded physical warehouse barcode counts against website database balances. If a discrepancy is detected, the pipeline immediately generates an automated mismatch alert for the warehouse team at 08:00 AM so they can investigate and correct shelf numbers before online shoppers order items that are physically sold out.

## Alternatives considered

### Alternative A: Build a continuous streaming pipeline using Apache Kafka and live stream engines

- **How it would work:** Every mouse click, cart update, order placement, and delivery change is published as a continuous stream of events into a messaging broker (such as Apache Kafka). A streaming software engine calculates running metrics second by second.
- **Why it is attractive:** It produces dashboards that update every few seconds, which impresses investors and fulfills the board's interest in live data.
- **Why rejected:** We apply the operational test: _"What business decision changes if this number is 10 seconds old instead of 24 hours old?"_ Managing Director meetings, Nana's operational reviews, and Finance's bank balancing do not happen second by second. Paying for continuous streaming servers wastes money on servers sitting around waiting during quiet hours. More importantly, streaming introduces complex failure points (such as duplicate messages, out-of-order records, and network drops) that would overwhelm a two-person engineering team. Daily batch processing gives 100% of the decision value at a fraction of the operational headache.

### Alternative B: Pure 100% daily batch processing with zero real-time exceptions (including inventory)

- **How it would work:** Everything without exception, including inventory stock levels, is updated only once every night at 02:00 AM.
- **Why it is attractive:** Extremely simple architecture because every single record in the business follows one single daily batch pipeline.
- **Why rejected:** Kloud Kart ships 4,000 orders per day. If product availability numbers update only once every 24 hours, the website shows yesterday's stock. Multiple customers browsing simultaneously will buy items that are physically sold out in the warehouse. This causes overselling, angry customer calls, bank refund processing fees, and damaged brand reputation. Inventory reservation must stay live on the primary store database.

## Consequences

- **What this buys:** Predictable, reliable daily pipelines that are easy to test, monitor, and rerun if a glitch happens. No midnight alerts waking engineers up. Accurate shelf stock that permanently prevents overselling cancellations, backed by automated daily stock drift alerts that catch and correct warehouse inventory mismatches before customers checkout.
- **What this costs:** Board Members must accept that operational dashboards show sales up to the close of business yesterday (up to 24 hours old).
- **What it costs the client if I am wrong:** If the Marketing team runs intense flash sales that require adjusting social media ad spending every 30 minutes, they will lack hourly sales feedback during that single day.
- **What would make me revisit this:** Daily sales scaling beyond 25,000 orders per day across several West African countries; automated pricing software requiring live competitor price tracking; or automated warehouse robotics requiring millisecond routing updates.

## What this survives

This decision comfortably survives growth up to 10,000 orders per day across Ghana and Nigeria. It protects storefront checkout integrity while keeping operating costs and engineering workload strictly bounded.
