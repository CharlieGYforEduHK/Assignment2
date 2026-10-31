"""
Unit tests for Problem 3: Order

Instructions:
Complete the unit test methods below using Python's unittest framework.
Your test methods must assert MULTIPLE ATTRIBUTES on the Order object
(e.g., subtotal, discount_amount, tax_amount, shipping_fee, final_total, status)
to verify state consistency under various conditions.

Running tests:
    python -m unittest test_problem3.py -v
"""
import unittest
from problem3 import Order


class TestOrder(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.regular_order = Order("ORD100", customer_tier="regular")
        self.silver_order = Order("ORD200", customer_tier="silver")
        self.gold_order = Order("ORD300", customer_tier="gold")

    # TODO: develop 5 test methods for Order class

    def test_add_items_updates_order_attributes(self):
        """
        Test adding taxable and grocery items and verify recalculated state.
        """
        self.regular_order.add_item(
            "Laptop",
            price=20,
            quantity=2,
            category="electronics"
        )
        self.regular_order.add_item(
            "Apple",
            price=10,
            quantity=1,
            category="grocery"
        )

        # Subtotal = 20 * 2 + 10 = 50
        # Taxable amount = 20 * 2 = 40
        # Tax = 40 * 8% = 3.20
        # Shipping is free because net subtotal is at least 50
        # Final total = 50 + 3.20 = 53.20
        self.assertEqual(self.regular_order.subtotal, 50.0)
        self.assertEqual(self.regular_order.discount_amount, 0.0)
        self.assertEqual(self.regular_order.tax_amount, 3.20)
        self.assertEqual(self.regular_order.shipping_fee, 0.0)
        self.assertEqual(self.regular_order.final_total, 53.20)
        self.assertEqual(self.regular_order.status, "PENDING")

        self.assertEqual(len(self.regular_order.items), 2)
        self.assertEqual(self.regular_order.items["Laptop"]["quantity"], 2)
        self.assertEqual(self.regular_order.items["Apple"]["category"], "grocery")

        summary = self.regular_order.get_summary()
        self.assertEqual(summary["order_id"], "ORD100")
        self.assertEqual(summary["tier"], "regular")
        self.assertEqual(summary["item_count"], 3)
        self.assertEqual(summary["subtotal"], 50.0)
        self.assertEqual(summary["final_total"], 53.20)
        self.assertEqual(summary["status"], "PENDING")

    def test_silver_tier_discount_tax_and_free_shipping(self):
        """
        Test silver membership discount, tax calculation, and free shipping.
        """
        self.silver_order.add_item(
            "Monitor",
            price=100,
            quantity=1,
            category="electronics"
        )

        # Silver discount = 100 * 5% = 5
        # Net subtotal = 95
        # Tax = 95 * 8% = 7.60
        # Shipping = 0 because net subtotal >= 50
        # Final total = 95 + 7.60 = 102.60
        self.assertEqual(self.silver_order.customer_tier, "silver")
        self.assertEqual(self.silver_order.subtotal, 100.0)
        self.assertEqual(self.silver_order.discount_amount, 5.0)
        self.assertEqual(self.silver_order.tax_amount, 7.60)
        self.assertEqual(self.silver_order.shipping_fee, 0.0)
        self.assertEqual(self.silver_order.final_total, 102.60)
        self.assertEqual(self.silver_order.status, "PENDING")

        summary = self.silver_order.get_summary()
        self.assertEqual(summary["tier"], "silver")
        self.assertEqual(summary["item_count"], 1)
        self.assertEqual(summary["discount_amount"], 5.0)
        self.assertEqual(summary["final_total"], 102.60)

    def test_gold_tier_and_save10_coupon(self):
        """
        Test gold membership discount combined with SAVE10 coupon.
        """
        self.gold_order.add_item(
            "Phone",
            price=100,
            quantity=1,
            category="electronics"
        )
        self.gold_order.apply_coupon(" save10 ")

        # Gold discount = 100 * 10% = 10
        # Remaining subtotal = 90
        # SAVE10 discount = 90 * 10% = 9
        # Total discount = 19
        # Net subtotal = 81
        # Tax = 81 * 8% = 6.48
        # Final total = 81 + 6.48 = 87.48
        self.assertEqual(self.gold_order.applied_coupon, "SAVE10")
        self.assertEqual(self.gold_order.subtotal, 100.0)
        self.assertEqual(self.gold_order.discount_amount, 19.0)
        self.assertEqual(self.gold_order.tax_amount, 6.48)
        self.assertEqual(self.gold_order.shipping_fee, 0.0)
        self.assertEqual(self.gold_order.final_total, 87.48)
        self.assertEqual(self.gold_order.status, "PENDING")

        summary = self.gold_order.get_summary()
        self.assertEqual(summary["tier"], "gold")
        self.assertEqual(summary["discount_amount"], 19.0)
        self.assertEqual(summary["tax_amount"], 6.48)
        self.assertEqual(summary["final_total"], 87.48)

    def test_remove_item_recalculates_order(self):
        """
        Test removing part of an item's quantity and verify recalculation.
        """
        self.regular_order.add_item(
            "Book",
            price=15,
            quantity=3,
            category="books"
        )

        self.assertEqual(self.regular_order.subtotal, 45.0)
        self.assertEqual(self.regular_order.items["Book"]["quantity"], 3)

        self.regular_order.remove_item("Book", quantity=1)

        # Remaining subtotal = 15 * 2 = 30
        # Tax = 30 * 8% = 2.40
        # Shipping = 5.99
        # Final total = 30 + 2.40 + 5.99 = 38.39
        self.assertEqual(self.regular_order.subtotal, 30.0)
        self.assertEqual(self.regular_order.discount_amount, 0.0)
        self.assertEqual(self.regular_order.tax_amount, 2.40)
        self.assertEqual(self.regular_order.shipping_fee, 5.99)
        self.assertEqual(self.regular_order.final_total, 38.39)
        self.assertEqual(self.regular_order.items["Book"]["quantity"], 2)
        self.assertEqual(self.regular_order.status, "PENDING")

        summary = self.regular_order.get_summary()
        self.assertEqual(summary["item_count"], 2)
        self.assertEqual(summary["subtotal"], 30.0)
        self.assertEqual(summary["shipping_fee"], 5.99)
        self.assertEqual(summary["final_total"], 38.39)

    def test_status_transitions_and_invalid_operations(self):
        """
        Test checkout, cancellation, frozen modifications, and invalid inputs.
        """
        # Empty order cannot be checked out
        with self.assertRaises(ValueError):
            self.regular_order.checkout()

        self.assertEqual(self.regular_order.status, "PENDING")
        self.assertEqual(self.regular_order.subtotal, 0.0)
        self.assertEqual(self.regular_order.final_total, 0.0)

        # Add an item and successfully check out
        self.regular_order.add_item(
            "Keyboard",
            price=30,
            quantity=1,
            category="electronics"
        )

        self.assertTrue(self.regular_order.checkout())
        self.assertEqual(self.regular_order.status, "PAID")
        self.assertEqual(self.regular_order.subtotal, 30.0)
        self.assertEqual(self.regular_order.final_total, 38.39)

        # Paid orders cannot be modified or cancelled
        with self.assertRaises(RuntimeError):
            self.regular_order.add_item("Mouse", 10)

        with self.assertRaises(RuntimeError):
            self.regular_order.remove_item("Keyboard")

        with self.assertRaises(RuntimeError):
            self.regular_order.apply_coupon("SAVE10")

        with self.assertRaises(RuntimeError):
            self.regular_order.cancel()

        self.assertEqual(self.regular_order.status, "PAID")
        self.assertEqual(len(self.regular_order.items), 1)
        self.assertEqual(self.regular_order.get_summary()["status"], "PAID")

        # Invalid constructor tier
        with self.assertRaises(ValueError):
            Order("ORD999", customer_tier="platinum")

        # Invalid item values
        pending_order = Order("ORD400")

        with self.assertRaises(ValueError):
            pending_order.add_item("Invalid Price", price=0)

        with self.assertRaises(ValueError):
            pending_order.add_item("Invalid Quantity", price=10, quantity=0)

        with self.assertRaises(KeyError):
            pending_order.remove_item("Missing Item")

        with self.assertRaises(ValueError):
            pending_order.apply_coupon("UNKNOWN")

        self.assertEqual(pending_order.status, "PENDING")
        self.assertEqual(pending_order.items, {})
        self.assertEqual(pending_order.subtotal, 0.0)
        self.assertEqual(pending_order.final_total, 0.0)


if __name__ == "__main__":
    unittest.main()
