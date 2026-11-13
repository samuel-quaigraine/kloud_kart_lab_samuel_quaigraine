# Kloud Kart Act 843 Customer Data Copy Inventory and Deletion Register

**Document Custodian:** Nana Adjei, Head of Operations  
**Regulatory Framework:** Ghana Data Protection Act, 2012 (Act 843)  
**Status:** Active Operational Register  
**Operational Scope:** Cross-departmental inventory of personal customer data copies, statutory deletion tracking, and Monday revenue sign-off protocol.

---

## 1. Operational Purpose

Under Ghana's Data Protection Act, 2012 (Act 843), as I understand it, individuals have the legal right to request the deletion or correction of their personal data (with statutory handling generally requiring response within 21 calendar days). Kloud Kart faces an active complaint forwarded by the Data Protection Commission (DPC) regarding a customer deletion request. Company leadership has established a strict 90-day internal implementation period (Quarter 1, Months 1 to 3) to locate and retire historical spreadsheets, deploy automated privacy masking, implement a permanent deletion audit log, and formally resolve the active DPC complaint with verified audit proof.

Technical database architecture alone cannot clean up unmanaged spreadsheets already saved on employee laptops. This register provides Nana Adjei with a non-technical, repeatable management tool to:
1. Locate and inventory every copy of customer personal data across all departments.
2. Track and verify customer deletion requests to complete compliance within the mandatory 90-day implementation period, including permanent erasure protection across system backup restores.
3. Maintain a permanent, tamper-evident deletion audit log that proves regulatory compliance to the DPC while supporting targeted recovery if an account was flagged in error (recovering transaction history via anonymous reference codes without resurrecting private personal data).
4. Reconcile and sign off on Monday revenue figures between Operations and Finance without circular arguments.

---

## 2. Customer Data Copy Inventory

The table below catalogs every known location where personal customer details (names, phone numbers, email addresses, and physical delivery addresses) exist across Kloud Kart:

| Copy ID | Storage Location | Department Custodian | Specific Personal Data Fields | Storage Format | Current Risk Level | Mandatory Retirement Action |
|---|---|---|---|---|---|---|
| **LOC-01** | Nana's Personal Laptop Downloads (`C:\Users\Nana\Downloads\orders_export_*.csv`) | Operations (Nana Adjei) | Customer full names, delivery addresses, phone numbers, order amounts. | Plain comma-separated values (CSV) files | **CRITICAL** (Unsecured, unencrypted) | Purge historical files immediately. Redirect all future reporting to the duplicate mirror server using masked customer identification numbers (IDs). |
| **LOC-02** | Marketing Team Workstations (`300k_customers_master.xlsx`) | Marketing Team | 300,000 customer names, phone numbers, email addresses, delivery regions. | Excel Spreadsheets | **CRITICAL** (Untracked local spreadsheet copies) | Revoke raw downloads. Provide marketing with an aggregated, anonymized dashboard view showing cohort metrics without plain contact info. |
| **LOC-03** | Finance Weekly Settlement Ledgers (`finance_reconciliation_2026.xlsx`) | Finance Department | Customer names, payment card references, mobile money numbers, transaction totals. | Excel Spreadsheets | **HIGH** (Unencrypted local storage) | Standardize finance reports on transaction IDs and settlement timestamps; strip customer personal names and telephone numbers. |
| **LOC-04** | Shared Desktop Drives and Ad-Hoc Team Exports | Staff across Operations, Finance, and Marketing | Ad-hoc customer extracts, order verification notes, customer telephone lists. | Local CSV files and desktop spreadsheets | **MEDIUM** (Unmanaged files on local storage) | Enforce mandatory deletion policy for all local export files older than 7 days once masked reporting views are deployed. |
| **LOC-05** | Production Database Server Snapshots (`/backups/mysql_dump_*.sql.gz`) | Sole Developer | Complete operational database tables including plain customer passwords and addresses. | Compressed SQL dumps | **MEDIUM** (On-server backup storage) | Encrypt backup files at rest. Include automated deletion-log re-application in all database recovery procedures. |

---

## 3. Permanent Deletion Audit Log and DPC Response Register

This register permanently records every formal customer data deletion request (tracking anonymous customer reference codes, dates, and deletion reasons without storing private contact details), and verifies erasure across all copy locations:

| Request ID | Receipt Date | Customer Identifier (Masked) | Deletion Reason | Target Completion Date | Store Database Erased | Marketing List Purged | Operations Downloads Cleared | Shared Team Copies Cleared | Backup Re-Application Verified | Verification Sign-Off | Compliance Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **DPC-2026-001** *(Active DPC Complaint)* | 2026-10-15 | `cust_ref_08491` (Complaining Customer) | Account closure & erasure request | 2026-01-13 (Day 90 Sprint) | Yes (Deleted 2026-10-18) | Pending (Target: Day 60) | Pending (Target: Day 60) | Yes (Scrubbed 2026-10-20) | Yes (Enrolled in restore script) | Nana Adjei | **IN PROGRESS** (On schedule to resolve DPC complaint) |
| **DPC-2026-002** | 2026-11-02 | `cust_ref_11204` | Customer marketing opt-out | 2026-01-31 (Day 90 Sprint) | Yes (Deleted 2026-11-04) | Pending (Target: Day 45) | Pending (Target: Day 45) | Yes (Scrubbed 2026-11-05) | Yes (Enrolled in restore script) | Nana Adjei | **IN PROGRESS** |
| **DPC-2026-003** *(Simulated Audit Test)* | 2026-11-10 | `cust_ref_test_001` | Practice regulatory audit drill | 2026-02-08 (Day 90 Sprint) | Yes (Deleted 2026-11-10) | Yes (Purged 2026-11-11) | Yes (Purged 2026-11-11) | Yes (Scrubbed 2026-11-11) | Yes (Verified post-restore) | Nana Adjei | **VERIFIED COMPLIANT** (Full audit trail confirmed) |

### Targeted Recovery Safeguard:
If an account or order is ever flagged for deletion by mistake, this permanent audit log allows targeted operational recovery of the anonymous transaction history (linking orders to `DIM_CUSTOMER_ANONYMOUS` via surrogate keys) while ensuring that deleted personal contact details (names, phone numbers, and physical addresses) remain permanently erased and unrecoverable, preserving complete compliance under Act 843.

### 6-Step Verification Protocol for Deletion Requests:
1. **Log & Timestamp:** Log the customer reference code, request date, and reason in the permanent deletion audit log to start the compliance clock.
2. **Primary Store Erase:** The developer executes a soft-delete and sets `deleted_at` on the live MySQL store database.
3. **Reporting Schema Verification:** Verify that nightly ingestion scrubs personal identifiers and only stores the irreversible anonymous reference.
4. **Local Copy Purge:** Confirm that staff across Operations, Finance, and Marketing have deleted any local spreadsheet extracts containing this customer.
5. **Backup Restore Safeguard:** Append the customer reference code to the permanent Automated Deletion List so that whenever an older system backup is restored during disaster recovery, the post-restore clean-up routine immediately re-deletes the customer's personal details before the database goes live.
6. **Final Sign-Off:** Nana Adjei signs the verification log and files the response certificate for the Data Protection Commission.

---

## 4. Monday Revenue and Variance Sign-Off Protocol

To end the weekly circular debates between Operations and Finance, both department leads complete this sign-off sheet every Monday morning before the executive management meeting:

| Week Beginning | Operations Dispatched Revenue | Finance Bank-Settled Revenue | Variance Delta | Primary Reason for Variance | Operations Sign-off | Finance Sign-off | Executive Status |
|---|---|---|---|---|---|---|---|
| **2026-11-02** | GH₵ 1,420,500 | GH₵ 1,310,200 | GH₵ 110,300 | Normal 48-hour weekend bank clearing window; 314 cash-on-delivery orders in transit with couriers. | N. Adjei | Finance Lead | **APPROVED** (Timing variance verified) |
| **2026-11-09** | GH₵ 1,395,800 | GH₵ 1,388,400 | GH₵ 7,400 | Minor card gateway settlement fee timing; 18 returned items pending inspection. | N. Adjei | Finance Lead | **APPROVED** (Within 1% tolerance) |
| **2026-11-16** | GH₵ 1,460,000 | GH₵ 1,340,000 | GH₵ 120,000 | Weekend flash sale orders placed Sunday night awaiting Monday courier pickup. | Pending | Pending | **PENDING REVIEW** |

