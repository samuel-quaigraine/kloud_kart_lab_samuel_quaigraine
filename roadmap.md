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
  - **WHAT changes:** Staff across Operations, Finance, and Marketing stop downloading unmanaged customer CSVs to local computers and access masked reporting views instead. A repeatable deletion process scrubs requested customer identifiers across live store and reporting tables within 90 days.
  - **HOW it is verified:** Before Day 90, Nana confirms that existing customer CSVs are cleared from staff computers across Operations, Finance, and Marketing, DPC registration renewal is submitted, and searching a test deleted customer ID in the reporting dashboard returns zero personal contact details.

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

## Quarter 3: Regional Expansion and Departmental Self-Service (Months 7 to 9)

**Guiding Principle:** Isolate regional pilot data and remove engineering bottlenecks from routine reporting.

- **Outcome 3.1: Isolated Reporting for the Nigeria Market Pilot**
  - **WHO is better off:** Regional Expansion Manager and Board of Directors.
  - **WHAT changes:** Performance numbers for Nigeria (order volume, delivery success rates, and local currency totals) are separated cleanly from Ghana core operations.
  - **HOW it is verified:** By September 30, the board dashboard includes a dedicated Nigeria tab displaying separate order conversion and delivery timelines without contaminating Ghana revenue metrics.
- **Outcome 3.2: Departmental Self-Service Reporting**
  - **WHO is better off:** Operations supervisors, Warehouse managers, and Marketing leads.
  - **WHAT changes:** Department leads generate their own routine operational summaries using pre-built report views rather than submitting data requests to the developer.
  - **HOW it is verified:** By September 30, department leads produce their required monthly reports independently without filing technical support tickets.

---

## Quarter 4: Inventory Observability and Deletion Auditing (Months 10 to 12)

**Guiding Principle:** Protect against warehouse overselling and ensure disaster recovery respects privacy deletions.

- **Outcome 4.1: Warehouse Shelf-to-Database Stock Drift Alerting**
  - **WHO is better off:** Warehouse Inventory Manager, Customer Service Team, and online shoppers.
  - **WHAT changes:** Discrepancies between physical shelf counts and website stock counts are flagged before an oversold item triggers a customer refund.
  - **HOW it is verified:** By December 15, inventory logs confirm that stock discrepancies caught prior to customer purchase exceed 95%, reducing overselling cancellation tickets to under 0.5% of total volume.
- **Outcome 4.2: Customer Deletion Protection Across Backup Restores**
  - **WHO is better off:** Kloud Kart Leadership and customers who requested data deletion.
  - **WHAT changes:** Any system backup recovery automatically re-applies the customer deletion list so erased customer details can never accidentally reappear.
  - **HOW it is verified:** By December 20, Nana receives a signed restoration test certificate showing that after a test backup recovery, searching a previously deleted customer ID in the reporting dashboard returns zero personal records.
