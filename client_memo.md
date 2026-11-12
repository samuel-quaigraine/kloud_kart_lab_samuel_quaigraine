# Memo to Nana

**From:** Lead Data Engineering Consultant  
**Date:** November 12, 2026  
**Subject:** Kloud Kart Data Strategy & Deliverables  

---

## What I found

Your current setup is breaking down because our live online store and our company database share a single physical computer. When you download weekly reports on Monday mornings, you compete directly with shoppers trying to buy products, which caused the website to freeze twice last month. 

Furthermore, you and the Finance team calculate weekly revenue using different spreadsheets with different formulas, which is why your numbers never match. 

Finally, our customer lists are currently downloaded onto personal laptops without oversight. Under Ghanaian data privacy law, if a customer requests that their records be deleted, we have ninety days to locate and delete every single copy. With files scattered across staff computers, we cannot currently pass a regulatory audit.

---

## What I built

| What you asked for | Status | Evidence |
|---|---|---|
| **Stop website crashes during reports** | Delivered | Designed the workload separation using our pre-approved duplicate server so reporting never touches live shoppers. |
| **Resolve the revenue disagreement with Finance** | Delivered | Built and verified an automated daily reconciliation engine (`src/reconciliation_audit.py`) that matches orders to bank settlements. |
| **A defensible twelve-month roadmap** | Delivered | Formulated a quarterly roadmap (`roadmap.md`) where every milestone is verifiable by you without asking an engineer. |
| **Five formal decision records** | Delivered | Documented five decision records (`decisions/ADR-001` through `ADR-005`) explaining every architectural choice and rejected alternative. |
| **A board-ready presentation with zero technical jargon** | Delivered | Created an eight-slide presentation (`presentation/board_presentation.md`) with complete speaking notes for your board meeting. |
| **An improvement beyond what was asked** | Delivered | Built an automated morning alert tool that catches warehouse inventory count errors before customers can buy out-of-stock items. |

---

## What I recommend

1. **Activate the Pre-Approved Duplicate Server:** Point all weekly reporting and data extracts to this second machine immediately to protect website performance.
2. **Standardize Business Metrics in Database Queries:** Replace personal spreadsheet formulas with an agreed-upon revenue query so Operations and Finance read from one single source of truth.
3. **Protect Customer Privacy at the Gate:** Strip out customer names, phone numbers, and addresses before data enters the reporting system, keeping our privacy audit footprint tiny and fully compliant with Ghanaian law.
4. **Sequence Hiring by Operational Priority:** Hire a Data Engineer first to automate data transfers and protect the shop, followed by an Analytics Engineer to model business reporting.

---

## What I could not stand behind

- **Building an Enterprise Data Lakehouse:** Suggested by investors, but lakehouses are designed for massive companies managing petabytes of video and audio files. For our forty gigabytes of structured retail data, it would create unmanageable complexity.
- **Real-Time Streaming Dashboards:** Monitoring a business second-by-second changes no management decisions and costs significant money. Daily updates satisfy ninety-nine percent of our business needs. The only number that must be real-time is physical warehouse stock.
- **Hiring for Artificial Intelligence Demand Forecasting:** Predictive algorithms require clean, trusted historical data. Forecasting demand on top of uncleaned inventory counts and disputed revenue figures is an expensive distraction that we must decline until foundational data is reliable.
