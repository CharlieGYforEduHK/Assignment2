"""
Unit tests for Problem 2: BankAccount

Instructions:
Complete the unit test methods below using Python's unittest framework.
Your test methods must assert MULTIPLE ATTRIBUTES on the BankAccount object
(e.g., balance, status, transaction_history, summary) to verify state consistency.

Running tests:
    python -m unittest test_problem2.py -v
"""
import unittest
from problem2 import BankAccount


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.account_empty = BankAccount("ACC001", "Alice", initial_balance=0.0, overdraft_limit=100.0)
        self.account_funded = BankAccount("ACC002", "Bob", initial_balance=200.0, overdraft_limit=50.0)

    def test_initial_state_multi_attributes(self):
        """
        Verify that a newly created account initializes all attributes correctly.
        Check balance, owner, status, overdraft_limit, transaction_history, and summary.
        """
        # Test empty account
        # TODO: implement it
        self.assertEqual(self.account_empty.account_id, "ACC001")
        self.assertEqual(self.account_empty.owner, "Alice")
        self.assertEqual(self.account_empty.balance, 0.0)
        self.assertEqual(self.account_empty.overdraft_limit, 100.0)
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(self.account_empty.transaction_history, [])

        empty_summary = self.account_empty.get_summary()
        self.assertEqual(empty_summary["account_id"], "ACC001")
        self.assertEqual(empty_summary["owner"], "Alice")
        self.assertEqual(empty_summary["balance"], 0.0)
        self.assertEqual(empty_summary["status"], "ACTIVE")
        self.assertEqual(empty_summary["overdraft_limit"], 100.0)
        self.assertEqual(empty_summary["transaction_count"], 0)

        # Test funded account
        # TODO: implement it
        self.assertEqual(self.account_funded.account_id, "ACC002")
        self.assertEqual(self.account_funded.owner, "Bob")
        self.assertEqual(self.account_funded.balance, 200.0)
        self.assertEqual(self.account_funded.overdraft_limit, 50.0)
        self.assertEqual(self.account_funded.status, "ACTIVE")
        self.assertEqual(len(self.account_funded.transaction_history), 1)

        initial_transaction = self.account_funded.transaction_history[0]
        self.assertEqual(initial_transaction["type"], "INITIAL_DEPOSIT")
        self.assertEqual(initial_transaction["amount"], 200.0)
        self.assertEqual(initial_transaction["fee"], 0.0)
        self.assertEqual(initial_transaction["balance_after"], 200.0)

        funded_summary = self.account_funded.get_summary()
        self.assertEqual(funded_summary["account_id"], "ACC002")
        self.assertEqual(funded_summary["owner"], "Bob")
        self.assertEqual(funded_summary["balance"], 200.0)
        self.assertEqual(funded_summary["status"], "ACTIVE")
        self.assertEqual(funded_summary["overdraft_limit"], 50.0)
        self.assertEqual(funded_summary["transaction_count"], 1)
        
        #pass

    def test_deposit_updates_multiple_attributes(self):
        """
        Test that deposit correctly updates balance, transaction_history, and summary.
        """
        # TODO: Implement test: deposit $150 into self.account_empty
        result = self.account_empty.deposit(150)

        self.assertTrue(result)
        self.assertEqual(self.account_empty.balance, 150.0)
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(len(self.account_empty.transaction_history), 1)

        transaction = self.account_empty.transaction_history[0]
        self.assertEqual(transaction["type"], "DEPOSIT")
        self.assertEqual(transaction["amount"], 150.0)
        self.assertEqual(transaction["fee"], 0.0)
        self.assertEqual(transaction["balance_after"], 150.0)

        summary = self.account_empty.get_summary()
        self.assertEqual(summary["balance"], 150.0)
        self.assertEqual(summary["status"], "ACTIVE")
        self.assertEqual(summary["transaction_count"], 1)

        #pass

    def test_withdrawal_within_balance_multi_attributes(self):
        """
        Test withdrawal when sufficient positive balance exists.
        """
        # TODO: Implement test: withdraw $50 with a $2.50 fee from self.account_funded
        result = self.account_funded.withdraw(50, fee=2.50)

        self.assertTrue(result)
        self.assertEqual(self.account_funded.balance, 147.50)
        self.assertEqual(self.account_funded.status, "ACTIVE")
        self.assertEqual(len(self.account_funded.transaction_history), 2)

        transaction = self.account_funded.transaction_history[-1]
        self.assertEqual(transaction["type"], "WITHDRAWAL")
        self.assertEqual(transaction["amount"], 50.0)
        self.assertEqual(transaction["fee"], 2.50)
        self.assertEqual(transaction["balance_after"], 147.50)

        summary = self.account_funded.get_summary()
        self.assertEqual(summary["balance"], 147.50)
        self.assertEqual(summary["status"], "ACTIVE")
        self.assertEqual(summary["transaction_count"], 2)
        #pass

    def test_overdraft_withdrawal_and_status_transition(self):
        """
        Test withdrawal that uses overdraft protection (balance becomes negative but >= -overdraft_limit).
        """
        # TODO: Implement test: withdraw $50 from self.account_empty (which has 0 balance, limit 100)
        result = self.account_empty.withdraw(50)

        self.assertTrue(result)
        self.assertEqual(self.account_empty.balance, -50.0)
        self.assertEqual(self.account_empty.status, "OVERDRAWN")
        self.assertEqual(len(self.account_empty.transaction_history), 1)

        transaction = self.account_empty.transaction_history[0]
        self.assertEqual(transaction["type"], "WITHDRAWAL")
        self.assertEqual(transaction["amount"], 50.0)
        self.assertEqual(transaction["fee"], 0.0)
        self.assertEqual(transaction["balance_after"], -50.0)

        summary = self.account_empty.get_summary()
        self.assertEqual(summary["balance"], -50.0)
        self.assertEqual(summary["status"], "OVERDRAWN")
        self.assertEqual(summary["transaction_count"], 1)
        #pass

    def test_deposit_recovering_from_overdrawn_status(self):
        """
        Test that depositing enough money to bring balance >= 0 transitions status from OVERDRAWN to ACTIVE.
        """
        # TODO: Implement test
        self.account_empty.withdraw(50)
        result = self.account_empty.deposit(50)

        self.assertTrue(result)
        self.assertEqual(self.account_empty.balance, 0.0)
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(len(self.account_empty.transaction_history), 2)

        withdrawal = self.account_empty.transaction_history[0]
        deposit = self.account_empty.transaction_history[1]

        self.assertEqual(withdrawal["type"], "WITHDRAWAL")
        self.assertEqual(withdrawal["balance_after"], -50.0)
        self.assertEqual(deposit["type"], "DEPOSIT")
        self.assertEqual(deposit["amount"], 50.0)
        self.assertEqual(deposit["balance_after"], 0.0)

        summary = self.account_empty.get_summary()
        self.assertEqual(summary["balance"], 0.0)
        self.assertEqual(summary["status"], "ACTIVE")
        self.assertEqual(summary["transaction_count"], 2)
        #pass

    def test_transfer_between_accounts_multi_attributes(self):
        """
        Test fund transfer between two accounts.
        """
        # TODO: Implement test: transfer $50 from account_funded to account_empty with $5 fee
        result = self.account_funded.transfer_to(
            self.account_empty,
            50,
            transfer_fee=5
        )

        self.assertTrue(result)
         # Sender state
        self.assertEqual(self.account_funded.balance, 145.0)
        self.assertEqual(self.account_funded.status, "ACTIVE")
        self.assertEqual(len(self.account_funded.transaction_history), 2)

        sender_transaction = self.account_funded.transaction_history[-1]
        self.assertEqual(sender_transaction["type"], "WITHDRAWAL")
        self.assertEqual(sender_transaction["amount"], 50.0)
        self.assertEqual(sender_transaction["fee"], 5.0)
        self.assertEqual(sender_transaction["balance_after"], 145.0)

        # Recipient state
        self.assertEqual(self.account_empty.balance, 50.0)
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(len(self.account_empty.transaction_history), 1)

        recipient_transaction = self.account_empty.transaction_history[0]
        self.assertEqual(recipient_transaction["type"], "DEPOSIT")
        self.assertEqual(recipient_transaction["amount"], 50.0)
        self.assertEqual(recipient_transaction["fee"], 0.0)
        self.assertEqual(recipient_transaction["balance_after"], 50.0)

        # Summary state
        sender_summary = self.account_funded.get_summary()
        recipient_summary = self.account_empty.get_summary()

        self.assertEqual(sender_summary["balance"], 145.0)
        self.assertEqual(sender_summary["transaction_count"], 2)
        self.assertEqual(recipient_summary["balance"], 50.0)
        self.assertEqual(recipient_summary["transaction_count"], 1)
        #pass

    def test_frozen_account_restrictions(self):
        """
        Test that a FROZEN account rejects deposits, withdrawals, and transfers with RuntimeError.
        """
        # TODO: Implement test: freeze account and verify exceptions with self.assertRaises(RuntimeError)
        self.account_empty.freeze()

        self.assertEqual(self.account_empty.status, "FROZEN")
        self.assertEqual(self.account_empty.balance, 0.0)
        self.assertEqual(self.account_empty.transaction_history, [])

        with self.assertRaises(RuntimeError):
            self.account_empty.deposit(10)

        with self.assertRaises(RuntimeError):
            self.account_empty.withdraw(10)

        with self.assertRaises(RuntimeError):
            self.account_empty.transfer_to(self.account_funded, 10)

        self.assertEqual(self.account_empty.status, "FROZEN")
        self.assertEqual(self.account_empty.balance, 0.0)
        self.assertEqual(self.account_empty.transaction_history, [])

        self.account_empty.unfreeze()

        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(self.account_empty.balance, 0.0)
        self.assertEqual(len(self.account_empty.transaction_history), 0)
        #pass

    def test_invalid_operations_raise_exceptions(self):
        """
        Test exception handling
        """
        # TODO: Implement exception tests using self.assertRaises()
        # Invalid deposit amounts
        with self.assertRaises(ValueError):
            self.account_empty.deposit(0)

        with self.assertRaises(ValueError):
            self.account_empty.deposit(-10)

        # Invalid withdrawal amounts and fees
        with self.assertRaises(ValueError):
            self.account_funded.withdraw(0)

        with self.assertRaises(ValueError):
            self.account_funded.withdraw(-10)

        with self.assertRaises(ValueError):
            self.account_funded.withdraw(10, fee=-1)

        # Exceeding overdraft limit
        with self.assertRaises(ValueError):
            self.account_empty.withdraw(101)

        # Invalid transfer target
        with self.assertRaises(TypeError):
            self.account_funded.transfer_to("not an account", 10)

        # Invalid transfer amount
        with self.assertRaises(ValueError):
            self.account_funded.transfer_to(self.account_empty, 0)

        with self.assertRaises(ValueError):
            self.account_funded.transfer_to(self.account_empty, -10)

        # Verify that failed operations did not change account state
        self.assertEqual(self.account_empty.balance, 0.0)
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(self.account_empty.transaction_history, [])

        self.assertEqual(self.account_funded.balance, 200.0)
        self.assertEqual(self.account_funded.status, "ACTIVE")
        self.assertEqual(len(self.account_funded.transaction_history), 1)
        #pass


if __name__ == "__main__":
    unittest.main()
