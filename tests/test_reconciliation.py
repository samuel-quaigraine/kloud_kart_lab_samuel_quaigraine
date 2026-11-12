"""
Unit tests for Kloud Kart Automated Daily Revenue Reconciliation & Data Protection Audit Engine.
Uses standard library unittest so it runs in any standard Python environment.
"""

import unittest
from src.reconciliation_audit import (
    anonymize_email,
    sanitize_customer_record,
    audit_dataset_for_pii,
    reconcile_daily_revenue,
    detect_inventory_stock_drift,
)


class TestReconciliationAudit(unittest.TestCase):

    def test_anonymize_email(self):
        email = "kofi.mensah@example.com"
        hashed = anonymize_email(email)
        self.assertTrue(hashed.startswith("cust_"))
        self.assertEqual(len(hashed), 17)  # 'cust_' (5 chars) + 12 hex chars
        # Ensure deterministic output
        self.assertEqual(anonymize_email(email), hashed)
        # Ensure case-insensitivity
        self.assertEqual(anonymize_email("KOFI.MENSAH@EXAMPLE.COM"), hashed)

    def test_sanitize_customer_record_removes_forbidden_fields(self):
        raw_customer = {
            "customer_id": 1042,
            "full_name": "Ama Osei",
            "email": "ama.osei@gmail.com",
            "phone_number": "+233244123456",
            "delivery_address": "14 Ring Road Central, Accra",
            "region": "Greater Accra",
            "country": "Ghana",
            "created_date": "2026-05-10",
        }
        sanitized = sanitize_customer_record(raw_customer)
        
        self.assertNotIn("full_name", sanitized)
        self.assertNotIn("phone_number", sanitized)
        self.assertNotIn("delivery_address", sanitized)
        self.assertEqual(sanitized["source_customer_id"], 1042)
        self.assertTrue(sanitized["anonymous_account_code"].startswith("cust_"))
        self.assertEqual(sanitized["country_code"], "Ghana")
        self.assertEqual(sanitized["delivery_region"], "Greater Accra")

    def test_audit_dataset_for_pii_detects_violations(self):
        clean_dataset = [
            {"source_customer_id": 1, "anonymous_account_code": "cust_abc123456789", "country": "Ghana"},
            {"source_customer_id": 2, "anonymous_account_code": "cust_def987654321", "country": "Nigeria"},
        ]
        is_compliant, violations = audit_dataset_for_pii(clean_dataset)
        self.assertTrue(is_compliant)
        self.assertEqual(len(violations), 0)

        toxic_dataset = [
            {"customer_id": 1, "full_name": "Kwame Nkrumah", "email": "kwame@ghana.com"},
            {"customer_id": 2, "phone_number": "+233501234567"},
        ]
        is_compliant, violations = audit_dataset_for_pii(toxic_dataset)
        self.assertFalse(is_compliant)
        self.assertGreaterEqual(len(violations), 2)

    def test_reconcile_daily_revenue_matching(self):
        ops_orders = [
            {"order_id": 101, "status": "dispatched", "total_amount_ghs": 350.00},
            {"order_id": 102, "status": "delivered", "total_amount_ghs": 150.00},
            {"order_id": 103, "status": "pending_packing", "total_amount_ghs": 500.00},  # Excluded from revenue
        ]
        finance_settlements = [
            {"tx_id": 1, "settlement_status": "settled", "settled_amount_ghs": 350.00},
            {"tx_id": 2, "settlement_status": "settled", "settled_amount_ghs": 150.00},
        ]

        result = reconcile_daily_revenue(ops_orders, finance_settlements)
        self.assertTrue(result["is_reconciled"])
        self.assertEqual(result["operations_dispatched_revenue_ghs"], 500.00)
        self.assertEqual(result["finance_settled_revenue_ghs"], 500.00)
        self.assertEqual(result["variance_delta_ghs"], 0.0)
        self.assertEqual(result["reconciliation_status"], "MATCH")

    def test_reconcile_daily_revenue_variance_detected(self):
        ops_orders = [
            {"order_id": 101, "status": "dispatched", "total_amount_ghs": 750.00},
        ]
        finance_settlements = [
            {"tx_id": 1, "settlement_status": "settled", "settled_amount_ghs": 600.00},
        ]

        result = reconcile_daily_revenue(ops_orders, finance_settlements)
        self.assertFalse(result["is_reconciled"])
        self.assertEqual(result["variance_delta_ghs"], 150.00)
        self.assertEqual(result["reconciliation_status"], "VARIANCE_DETECTED")

    def test_detect_inventory_stock_drift(self):
        database_stock = {
            "SKU-SHOE-RED-42": 12,
            "SKU-BAG-LEATHER-BLK": 5,
            "SKU-WATCH-GOLD-01": 20,
        }
        physical_shelf_counts = {
            "SKU-SHOE-RED-42": 9,   # Drift of 3 (oversell risk)
            "SKU-BAG-LEATHER-BLK": 5,  # Matches
            "SKU-WATCH-GOLD-01": 0,  # Drift of 20 (critical oversell risk)
        }

        alerts = detect_inventory_stock_drift(database_stock, physical_shelf_counts)
        self.assertEqual(len(alerts), 2)
        
        sku_alerts = {a["sku"]: a for a in alerts}
        self.assertEqual(sku_alerts["SKU-SHOE-RED-42"]["oversell_risk_units"], 3)
        self.assertEqual(sku_alerts["SKU-SHOE-RED-42"]["severity"], "HIGH")
        self.assertEqual(sku_alerts["SKU-WATCH-GOLD-01"]["oversell_risk_units"], 20)
        self.assertEqual(sku_alerts["SKU-WATCH-GOLD-01"]["severity"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()
