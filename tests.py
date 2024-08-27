import unittest
from unittest import mock
import os
from main import Expense
from tracker import (
    expense_input, expense_to_file, check_reset_date, load_budget, save_budget, monthly_save)
from datetime import date

class TestTracker(unittest.TestCase):

    def setUp(self):
        self.finances_file = "test_finances.csv"
        self.latest_file = "latest_file.txt"
        self.budget_file = "test_budget.txt"
        with open(self.finances_file, "w") as f:
            f.write("")
        if os.path.exists(self.latest_file):
            os.remove(self.latest_file)
    
    def tearDown(self):
        self.clean_tests()

    def test_expese_input(self):
        inputs = ["Fruits", "8", "1"]
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            expense = expense_input()
            self.assertEqual(expense.name, "Fruits")
            self.assertEqual(expense.cost, 8)
            self.assertEqual(expense.type, "Groceries")
    
    def test_expense_to_file(self):
        expense = Expense(name="Gas", type="Transportation", cost=80.0, date="15-08-2024")
        expense_to_file(expense, self.finances_file)
        with open(self.finances_file, "r") as f:
            content = f.read()
            self.assertIn("Gas", content)
            self.assertIn("Transportation", content)
            self.assertIn("80.00", content)

    def save_percentages(category_budgets):
        with open("category_budgets.txt", "w") as f:
            for category, budget in category_budgets.items():
                f.write(f"{category}, {budget:.2f}\n")

    def test_check_reset_date(self):
        check_reset_date(self.finances_file)
        today = date.today().isoformat()
        self.assertTrue(os.path.exists(self.latest_file))
        with open(self.latest_file, "r") as f:
            last_date = f.read().strip()
            self.assertEqual(last_date, today)

    def test_load_save_budget(self):
        save_budget(100.0, self.budget_file)
        budget = load_budget(self.budget_file)
        self.assertEqual(budget, 100.0)

    def test_monthly_save(self):
        with open(self.finances_file, "w") as f:
            f.write("Example expense data")
        monthly_save(self.finances_file)
        time = date.today().strftime("%B_%Y")
        summary_file = f"expenses_{time}.csv"
        self.assertTrue(os.path.exists(summary_file))
        os.remove(summary_file)
    
    def clean_tests(self):
        for file in [self.finances_file, self.budget_file, self.latest_file]:
            if os.path.exists(file):
                os.remove(file)
        for file in os.listdir('.'):
            if file.startswith("expenses_" or file.endswith(".csv")):
                os.remove(file)

if __name__ == "__main__":
    unittest.main()