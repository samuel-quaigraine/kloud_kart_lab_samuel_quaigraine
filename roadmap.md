# Twelve-Month Data Roadmap: Kloud Kart

This roadmap is organized by quarterly business outcomes rather than internal engineering tasks. Every milestone passes the **Verification Test**: *Nana Adjei or the Finance Lead can verify that the outcome happened on their own, without needing to ask an engineer.*

---

## Quarter 1: Stop the Bleeding and Meet the 90-Day Privacy Deadline (Months 1 to 3)

**Guiding Principle:** Stop live website slowdowns and eliminate untracked customer data copies within the 90-day Data Protection Commission window.

- **Outcome 1.1: Storefront Speed Protected During Monday Reports**
  - **WHO is better off:** Online shoppers and Nana Adjei (Head of Operations).
  - **WHAT changes:** Weekly reporting queries move off the live shop server onto the duplicate reporting server. Monday exports no longer slow down customer checkouts.
  - **HOW it is verified:** On the first Monday of Month 2 at 09:00 AM, Nana runs her weekly report while placing a test checkout on the website; the page loads in under two seconds with zero customer slow-site complaints.
- **Outcome 1.2: Unmanaged Customer Spreadsheets Retired and 90-Day Deletion Operational**
  - **WHO is better off:** Kloud Kart leadership, staff across Operations, Finance, and Marketing, and customers exercising deletion rights.
  - **WHAT changes:** Staff across Operations, Finance, and Marketing stop downloading unmanaged customer comma-separated values (CSV) files to local computers and access masked reporting views instead. A repeatable deletion process scrubs requested customer identifiers across live store and reporting tables within 90 days.
  - **HOW it is verified:** Before Day 90, Nana confirms that existing customer CSV spreadsheets are cleared from staff computers across Operations, Finance, and Marketing, Data Protection Commission (DPC) registration renewal is submitted, and searching a test deleted customer identification number (ID) in the reporting dashboard returns zero personal contact details.

---

## Quarter 2: Establish the Single Source of Truth (Months 4 to 6)

**Guiding Principle:** Resolve the loudest business disagreement: the conflicting revenue numbers.

- **Outcome 2.1: Operations and Finance Report Identical Revenue**
  - **WHO is better off:** Nana Adjei (Operations) and the Finance Department Lead.
  - **WHAT changes:** Operations and Finance stop building private spreadsheet calculations. Both teams open a single automated dashboard that displays identical, verified daily and monthly revenue figures.
  - **HOW it is verified:** On April 30 at 08:30 AM, Nana and the Finance Lead open the monthly revenue summary; both screens display the exact same revenue number down to the last Ghana Cedi, matching bank gateway settlements.
- **Outcome 2.2: Automated Daily Discrepancy Alerting**
  - **WHO is better off:** Nana Adjei and the Managing Director.
  - **WHAT changes:** If an operational order and a bank payment fail to reconcile, an automated system alert is delivered before the start of the business day.
  - **HOW it is verified:** By June 15, an automated notification arrives in Nana's inbox every weekday morning at 08:00 AM confirming that all prior-day transactions reconciled with zero variance.

---

## Quarter 3: Separate Nigeria Tracking and Self-Serve Team Reports (Months 7 to 9)

**Guiding Principle:** Keep Nigeria pilot numbers separate from Ghana's core sales, and let department leads pull their own routine reports without waiting on the data team.

- **Outcome 3.1: Separate Reporting for the Nigeria Pilot**
  - **WHO is better off:** The Regional Expansion Manager and the Board of Directors.
  - **WHAT changes:** Nigeria orders, delivery success rates, and local-currency totals are tracked separately from Ghana's core sales, so early pilot tests do not distort Ghana's numbers.
  - **HOW it is verified:** By September 30, the board dashboard includes a dedicated Nigeria tab showing Nigeria's order counts, delivery timelines, and revenue totals completely separate from Ghana's totals.
- **Outcome 3.2: Ready-Made Reports for Department Leads**
  - **WHO is better off:** Nana Adjei (Head of Operations), Warehouse leads, and Marketing leads.
  - **WHAT changes:** Instead of asking the developer or data team to manually pull routine numbers, department leads open pre-built report views to check their own daily and monthly summaries.
  - **HOW it is verified:** By September 30, Operations, Warehouse, and Marketing leads generate their own monthly summaries directly from the reporting dashboard with zero manual data-export requests.

---

## Quarter 4: Stock Mismatch Alerts and Permanent Customer Deletions (Months 10 to 12)

**Guiding Principle:** Catch stock errors before customers buy out-of-stock items, and make sure deleted customer records stay erased even if we restore an old backup.

- **Outcome 4.1: Automatic Alerts When Warehouse Stock and Website Stock Do Not Match**
  - **WHO is better off:** Warehouse staff, the Customer Service team, and online shoppers.
  - **WHAT changes:** Whenever the physical count on the warehouse shelf disagrees with the stock number shown on the website, the system alerts the warehouse team immediately so they can fix it before a shopper orders an item we do not have.
  - **HOW it is verified:** By December 15, warehouse logs show that over 95% of stock mismatches are caught and corrected before a customer checks out, keeping out-of-stock order cancellations below 0.5% of total orders.
- **Outcome 4.2: Keeping Deleted Customers Erased After Backup Restores**
  - **WHO is better off:** Kloud Kart leadership (Nana Adjei) and customers who asked for their personal data to be deleted.
  - **WHAT changes:** Whenever the team restores an older system backup, an automatic clean-up step immediately re-deletes anyone on our deletion list so erased customer details never accidentally come back.
  - **HOW it is verified:** By December 20, Nana Adjei receives a signed test report proving that after a practice backup restore, searching for a deleted customer in the reporting dashboard returns zero personal records.
