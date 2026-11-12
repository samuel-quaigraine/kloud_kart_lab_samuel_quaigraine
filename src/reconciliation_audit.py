"""
Kloud Kart Automated Daily Revenue Reconciliation & Data Protection Audit Engine.

This tool solves two major operational problems for Nana Adjei:
1. Reconciles Operations dispatched orders against Finance payment gateway settlements
   to eliminate weekly revenue arguments before the start of the business day.
2. Audits analytical datasets to ensure zero raw, unmasked customer personal data 
   (Ghana Data Protection Act 843 compliance) has leaked into reporting tables.
3. Flags inventory discrepancies where database stock counts exceed physical shelf counts,
   preventing overselling before customer checkouts occur.
"""

from typing import Dict, List, Any, Tuple
import hashlib
import re


def anonymize_email(email: str) -> str:
    """Generate a one-way deterministic pseudonymous hash for customer email under Act 843."""
    if not email or not isinstance(email, str):
        return ""
    clean = email.strip().lower()
    return "cust_" + hashlib.sha256(clean.encode("utf-8")).hexdigest()[:12]


def sanitize_customer_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize customer record at the extraction boundary.
    Strips raw names, telephone numbers, and street addresses.
    Replaces email with anonymous account code.
    """
    sanitized = {
        "source_customer_id": record.get("customer_id"),
        "anonymous_account_code": anonymize_email(record.get("email", "")),
        "delivery_region": record.get("region", "Unknown"),
        "country_code": record.get("country", "Ghana"),
        "account_created_date": record.get("created_date"),
    }
    return sanitized


def audit_dataset_for_pii(records: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """
    Audit an analytical table to verify NO raw personal contact data exists.
    Returns (is_compliant, list_of_violations).
    """
    violations = []
    # Patterns for raw Ghanaian or Nigerian telephone numbers
    phone_pattern = re.compile(r"(\+?233|\+?234|0)\d{9,10}")
    email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    for idx, row in enumerate(records):
        for field, value in row.items():
            str_val = str(value)
            if field in ["full_name", "phone_number", "delivery_address", "street"]:
                violations.append(f"Row {idx}: Forbidden personal field '{field}' present.")
            if email_pattern.search(str_val):
                violations.append(f"Row {idx}: Unmasked raw email found in field '{field}'.")
            if phone_pattern.search(str_val):
                violations.append(f"Row {idx}: Unmasked telephone number found in field '{field}'.")

    is_compliant = len(violations) == 0
    return is_compliant, violations


def reconcile_daily_revenue(
    ops_orders: List[Dict[str, Any]], 
    finance_settlements: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Automated daily revenue reconciliation between Operations and Finance.
    
    Standardized Business Logic:
    - Operations Dispatched Revenue: Sum of all orders with status 'dispatched' or 'delivered'.
    - Finance Settled Revenue: Sum of all gateway transactions with status 'settled'.
    - In-Transit Revenue: Value of orders placed/dispatched pending bank settlement.
    """
    ops_dispatched_total = 0.0
    ops_dispatched_count = 0

    for order in ops_orders:
        status = order.get("status", "").lower()
        amount = float(order.get("total_amount_ghs", 0.0))
        if status in ["dispatched", "delivered"]:
            ops_dispatched_total += amount
            ops_dispatched_count += 1

    fin_settled_total = 0.0
    fin_settled_count = 0

    for tx in finance_settlements:
        status = tx.get("settlement_status", "").lower()
        amount = float(tx.get("settled_amount_ghs", 0.0))
        if status == "settled":
            fin_settled_total += amount
            fin_settled_count += 1

    delta = round(abs(ops_dispatched_total - fin_settled_total), 2)
    tolerance = 0.01  # Within 1 pesewa

    is_matched = delta <= tolerance

    return {
        "is_reconciled": is_matched,
        "operations_dispatched_revenue_ghs": round(ops_dispatched_total, 2),
        "operations_dispatched_order_count": ops_dispatched_count,
        "finance_settled_revenue_ghs": round(fin_settled_total, 2),
        "finance_settled_transaction_count": fin_settled_count,
        "variance_delta_ghs": delta,
        "reconciliation_status": "MATCH" if is_matched else "VARIANCE_DETECTED",
        "action_required": "None - figures match" if is_matched else f"Investigate variance of {delta} GHS",
    }


def detect_inventory_stock_drift(
    database_stock: Dict[str, int], 
    physical_shelf_counts: Dict[str, int]
) -> List[Dict[str, Any]]:
    """
    Compare website database stock numbers against physical warehouse shelf reality.
    Flags any product SKU where database stock exceeds physical shelf stock (risk of overselling).
    """
    drift_alerts = []

    for sku, db_count in database_stock.items():
        shelf_count = physical_shelf_counts.get(sku, 0)
        drift = db_count - shelf_count
        if drift > 0:
            drift_alerts.append({
                "sku": sku,
                "database_count": db_count,
                "physical_shelf_count": shelf_count,
                "oversell_risk_units": drift,
                "severity": "CRITICAL" if shelf_count == 0 else "HIGH",
                "recommended_action": f"Adjust database stock down by {drift} units immediately.",
            })

    return drift_alerts
