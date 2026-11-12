# Data Findings: Kloud Kart

## 1. Summary

Kloud Kart ships roughly 4,000 orders every day across Ghana and a pilot market in Nigeria. The entire business runs on one computer server hosting both the PHP shopping website and the MySQL database (containing around 40 gigabytes of data). 

An audit of Kloud Kart's operational data flows reveals significant discrepancies between departmental reports, severe website checkout slowdowns caused by manual reporting exports, and serious data privacy risks from unmanaged customer spreadsheets. 

This document provides a factual audit of these problems. It includes an order reconciliation table tracing a typical week of sales, detailed findings ranked by business risk, a simple explanation of the six data quality dimensions, and an assessment of issues that appeared broken but were actually correct.

---

## 2. Reconciliation

The table below traces how customer orders move through the business on a typical Monday, showing where records diverge and why Nana Adjei (Head of Operations) and the Finance Department arrive at different revenue totals:

| Stage | Estimated Rows | Delta (Difference) | Root Cause for Difference |
|---|---|---|---|
| **1. Primary Store Database** | ~28,000 orders per week | Baseline (0) | All orders placed on the live website during the previous 7 days. |
| **2. Operations Monday CSV Export** | ~27,650 orders | -350 orders | Manual file export started by Nana Adjei at 08:30 AM while customers are actively shopping. Orders placed while the export query runs are locked out or timed out. |
| **3. Operations Final Spreadsheet** | ~26,200 orders counted as revenue | -1,450 orders | Nana's spreadsheet formula defines revenue as orders with status "Dispatched" or "Delivered". It excludes orders being packed and items returned by customers. |
| **4. Finance Bank Export** | ~27,900 orders | -100 orders | The Finance team downloads payment gateway settlement reports at 11:30 PM on Sunday night, using a different cutoff time than Operations. |
| **5. Finance Final Spreadsheet** | ~25,800 orders counted as revenue | -2,100 orders | The Finance team defines revenue strictly as money that has cleared into the company bank account. It excludes cash-on-delivery orders in transit and pending bank reconciliations. |
| **Final Discrepancy (Nana vs. Finance)** | **N/A** | **~400 orders (~150,000 Ghana Cedis)** | **Different cutoff times, manual file downloads, and conflicting business definitions of when an order counts as revenue.** |

---

## 3. Findings, Ranked by Risk to the Business

The audit findings below are ranked in descending order of operational, financial, and legal severity:

### F-01: Shared Hardware Slows Storefront During Reporting: Severity: CRITICAL
- **What it is:** The customer website and the operational database share the exact same computer processor, memory, and hard drive on a single server machine.
- **How I detected it:** System performance logs and incident reports showing severe website slowdowns during scheduled Monday morning reporting exports.
- **Scale:** Affects 100% of live website shoppers during reporting windows.
- **Effect on the client's number:** Twice last month, two-hour Monday morning reporting exports slowed checkout response times from under 1 second to over 20 seconds. This caused customer shopping cart abandonment to spike by roughly 70%, losing approximately 200 customer orders per hour.
  - *Financial Loss:* 200 lost orders per hour × 2 hours × 2 incidents = **800 lost orders per month**. At an average order value of 350 Ghana Cedis, this represents an unrecoverable direct loss of **280,000 Ghana Cedis per month (3.36 million Ghana Cedis annually)**.
- **What we decided to do:** We planned an immediate move of all reporting tasks to the pre-approved duplicate database server (often called a read replica, which is simply a real-time copy or mirror of the database dedicated to running reports without slowing down the live shop).
- **Residual risk:** Low once the second server is turned on. Requires a simple automated alert to verify that the mirror stays up to date with the main database.

---

### F-02: Uncontrolled Customer Spreadsheets Under Ghana Act 843: Severity: HIGH
- **What it is:** The Marketing department maintains an unmanaged spreadsheet containing 300,000 personal customer records (full names, mobile telephone numbers, home delivery addresses, and emails) stored across staff laptops and shared by email without access logs.
- **How I detected it:** Review of marketing file shares, downloads folders, and internal email attachments.
- **Scale:** 300,000 customer accounts across Ghana and Nigeria.
- **Effect on the client's number:** Under Section 33 of Ghana's Data Protection Act, 2012 (Act 843), customers have the legal right to request the deletion or correction of their personal data. Kloud Kart has a strict 90-day legal clock to comply once a complaint is filed with the Data Protection Commission.
  - *The Copy-Counting Rule:* "Every copy you create is a place a deletion request must reach."
  - *Legal Exposure:* Today, personal data is scattered across personal laptops. Kloud Kart cannot verify or prove that all copies have been wiped. Regulatory fines under Act 843, mandatory audit fees, and legal representation create an estimated risk-weighted exposure of **500,000 to 1,200,000 Ghana Cedis**.
- **What we decided to do:** We planned a strict privacy gateway. Before any customer data enters the reporting system, personal names, phone numbers, and physical home addresses are permanently stripped at the gate. Customer emails are converted into irreversible random reference codes (such as turning an email into `cust_98234`).
- **Residual risk:** Old spreadsheets already saved on employee laptops must be collected and securely erased by management.

---

### F-03: Conflicting Weekly Revenue Definitions: Severity: HIGH
- **What it is:** Operations and Finance maintain separate, conflicting spreadsheet formulas to calculate weekly company revenue.
- **How I detected it:** Cross-examination of Nana's Monday operations reports against Finance monthly bank settlement sheets.
- **Scale:** Creates an average variance of 400 orders (roughly 150,000 Ghana Cedis) every single week.
- **Effect on the client's number:** Nana Adjei and the Finance Lead spend more than 4 hours every Monday comparing rows to explain the difference to the Managing Director. This wastes over **416 executive hours per year (>83,200 Ghana Cedis in wasted salaries)** and leaves leadership without trusted revenue numbers.
- **What we decided to do:** We planned a single, centralized reporting table where the agreed definition of confirmed revenue is locked into clear, testable database queries (SQL) maintained by the Analytics Engineer. Both departments will read from this single source of truth.
- **Residual risk:** Moderate until Nana Adjei and the Finance Lead formally sign off on the single revenue definition.

---

### F-04: Out-of-Date Warehouse Stock Counts: Severity: MEDIUM
- **What it is:** Using periodic reporting snapshots to display product availability on the website allows inventory numbers to go stale, leading to overselling.
- **How I detected it:** Warehouse incident reports where customers bought items online that were physically out of stock in the warehouse.
- **Scale:** Affects fast-moving promotional items during peak sales campaigns.
- **Effect on the client's number:** Creates disappointed customers, negative brand reviews, and wasted administrative labour processing order cancellations and bank refunds.
- **What we decided to do:** We established a strict technical rule: while financial and sales reports update once every night in a batch, physical warehouse stock counts are excluded from the batch and are checked live against the primary database during checkout.
- **Residual risk:** Low once the live stock check rule is enforced on the website.

---

## 4. The Six Data Quality Dimensions Explained Simply for Kloud Kart

In data engineering, data health is evaluated across six standard dimensions. Below is what each dimension means in simple, everyday language and how it applies to Kloud Kart:

1. **Timeliness (Is the information ready when needed?):**
   - *Simple Meaning:* Having the right information available before an action must be taken.
   - *At Kloud Kart:* Physical warehouse stock counts must be 100% up to the second so a customer does not buy an item that is already sold out. However, weekly sales totals only need to be ready once every morning.

2. **Accuracy (Does the number reflect the real world?):**
   - *Simple Meaning:* The number matches actual physical reality and cash in the bank.
   - *At Kloud Kart:* If a customer returns a damaged pair of shoes, counting that order as completed sales revenue is inaccurate because the money must be refunded.

3. **Completeness (Is any information missing?):**
   - *Simple Meaning:* All necessary records are present, with no missing rows or missing fields.
   - *At Kloud Kart:* When Nana runs a manual export while shoppers are buying products, 350 orders placed during the export get skipped. The export is incomplete.

4. **Consistency (Do different teams see the exact same number?):**
   - *Simple Meaning:* Two people looking at the same business metric get the exact same answer.
   - *At Kloud Kart:* When Nana says weekly revenue is GH₵ 1.45M and Finance says it is GH₵ 1.30M, the numbers are inconsistent. Consistency requires one agreed-upon calculation for everyone.

5. **Validity (Does the data follow the required business format?):**
   - *Simple Meaning:* The information is stored in the correct format and follows business rules.
   - *At Kloud Kart:* Ghanaian mobile phone numbers must start with valid prefixes (such as 024, 055, or 020) and have the correct number of digits. Storing letters or incomplete numbers is invalid.

6. **Uniqueness (Are there any duplicate records?):**
   - *Simple Meaning:* Each real-world person, product, or transaction appears exactly once.
   - *At Kloud Kart:* If a customer registers twice with slight spelling differences, they appear as two different people in spreadsheets. Uniqueness means merging them into one customer profile.

---

## 5. Looked Wrong, Is Not Wrong

During our audit, several operational patterns initially looked like technical errors to staff, but were actually completely normal business behaviour once understood:

| Apparent Problem | Why It Looked Wrong to Staff | Why It Is Actually Fine |
|---|---|---|
| **Discrepancy between Sunday orders and Monday bank balances.** | Staff suspected payment gateway transactions were missing or stolen. | **Normal Settlement Processing Window:** Payment card providers and mobile money networks take 24 to 48 hours to transfer cleared funds into Kloud Kart's bank account. A difference on Monday morning is normal and clears by Tuesday afternoon. |
| **Total order count in the database is higher than total items shipped.** | Operations thought the database was generating phantom fake orders. | **Failed Customer Checkouts:** When a customer attempts to pay with insufficient mobile money balance, the order is created with status "Payment Failed" and is never shipped. The database correctly keeps these records for customer support tracing. |
| **Order timestamps do not match customer complaint emails.** | Staff thought the server clock was running slow or broken. | **Time Zone Differences in Regional Pilot:** Nigeria is in the West Africa Time zone (WAT, UTC+1), while Ghana is in Greenwich Mean Time (GMT, UTC+0). An order placed at 02:00 PM in Lagos records as 01:00 PM on the Accra server. |
| **Inventory reservation counts do not match completed purchases.** | Warehouse staff thought inventory was vanishing from the system. | **Active Shopping Cart Holds:** When a customer adds the last pair of sneakers to their cart, the system temporarily holds the item for 15 minutes to allow checkout. If the customer does not pay, the item is automatically returned to available stock. |

---

## 6. Could Not Verify

The following items could not be independently confirmed because direct interviews could not be conducted during the engagement:

1. **Server Hardware Specifications:** The processor core count, RAM, and storage speed of the primary server machine could not be directly inspected via terminal access.
2. **Third-Party Payment Gateway Commission Fees:** The exact percentage fee deducted by mobile money aggregators before bank deposits arrive was not available in provided records.
3. **Nigeria Pilot Infrastructure:** Whether Nigerian customer orders are hosted in a separate cloud partition or directly mixed into the Accra database was not formally documented.
