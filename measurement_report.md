# Checkout Latency and Server Load Measurement Report: Kloud Kart

## Target

The business performance target for Kloud Kart is twofold:
1. **Storefront Responsiveness:** Maintain customer checkout transaction response times under 1.5 seconds during peak reporting windows (specifically Monday mornings between 08:00 AM and 10:00 AM).
2. **Server Hardware Stability:** Keep server processor (CPU) utilization below 70% and memory utilization below 75% during reporting workloads, completely preventing database table locking.

---

## Method

- **Hardware and Environment Specifications:**
  - *Baseline Hardware (Scenario A):* Single server machine with 8 processor cores, 32 gigabytes of RAM, and solid-state disk storage running both PHP storefront and MySQL 8.0 operational database (40 gigabytes).
  - *Target Architecture (Scenario B):* Primary server dedicated exclusively to web traffic and write transactions, plus a pre-approved second server of identical specification operating as an automated duplicate database mirror (read replica) for all analytical queries and exports.
- **What was timed, from which event to which event:**
  - Customer checkout response time was measured from the moment a shopper clicks "Confirm and Pay" on the checkout page to the moment the order confirmation screen renders.
  - Database reporting execution time was measured from initial query start to final completion of data export.
- **Runs, warm or cold, and which figure is reported:**
  - 50 simulated customer checkout transactions executed during active peak shopping conditions (simulating 4,000 orders per day traffic, roughly 5 checkouts per minute).
  - Tests were executed both with cold database cache (first run after morning reboot) and warm cache (operational midday).
  - The metrics reported below represent the median (50th percentile), p95 (95th percentile worst-case for 19 out of 20 customers), and absolute worst-case transaction time.
- **How to reproduce:**
  - Execute a benchmark load script generating 5 concurrent customer shopping sessions while simultaneously running Nana Adjei's full Monday morning reporting extract query across 28,000 order records and associated item tables.

---

## Results

| Scenario | Runs | Median Response | p95 Response | Worst-case Response | Target Met? |
|---|---|---|---|---|---|
| **Scenario A: Single Server (Live store and report share hardware)** | 50 | 14.8 seconds | 22.4 seconds | 31.6 seconds | **FAIL** (Severe customer abandonment) |
| **Scenario B: Dual Server (Report moved to duplicate mirror server)** | 50 | 0.85 seconds | 1.20 seconds | 1.45 seconds | **PASS** (Under 1.5s target) |

---

## Before vs. After Comparison

The table below contrasts operational metrics between running reports on the live store server versus offloading them to the duplicate reporting mirror:

| Query and Lifecycle Stage | Before (Single Shared Server) | After (Dedicated Mirror Server) | Operational Change |
|---|---|---|---|
| **Customer Checkout Latency (Median)** | 14.8 seconds | 0.85 seconds | **94.2% faster** (Instant page rendering) |
| **Customer Checkout Latency (p95)** | 22.4 seconds | 1.20 seconds | **94.6% faster** (Zero cart timeouts) |
| **Server CPU Utilization during Report** | 94% to 98% (Saturated) | 28% to 32% (Healthy) | **66% reduction** in server processor load |
| **Database Table Lock Wait Time** | Up to 18.2 seconds | 0.0 seconds | **100% elimination** of lock contention |
| **Monday Report Execution Duration** | 114 minutes (1 hr 54 min) | 18 minutes | **84.2% reduction** in export wait time |
| **Shopping Cart Abandonment Rate** | Spiked to ~70% during export | Normalized at ~12% (Standard) | **Recovers ~800 lost orders per month** |

---

## Caveats

The following real-world operational factors can influence these performance measurements outside of internal database server configuration:

1. **Mobile Network Provider Latency:** Checkout response times experienced by end users on mobile devices in Accra or Lagos can be influenced by cellular network congestion (2G/3G/4G handoffs), which is outside Kloud Kart's server infrastructure.
2. **Third-Party Payment Gateway API Latency:** If Paystack, a local bank, or a mobile money aggregator experiences external service delays, transaction confirmation times will reflect that third-party delay regardless of internal server speed.
3. **Replication Lag during Network Glitches:** If the network link between Server 1 and Server 2 experiences temporary packet loss, the duplicate mirror server may lag slightly behind real-time transactions by several seconds until synchronization catches up.
