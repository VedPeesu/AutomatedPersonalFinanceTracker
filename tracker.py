from main import Expense
from collections import defaultdict
import os
from datetime import date
from datetime import datetime
import matplotlib.pyplot as plt

def main():
    print(f"Finance Tracker")
    finance_file = "finance.csv"
    budget_file = "budget.txt"
    budget = load_budget(budget_file)
    check_reset_date(finance_file)

    while True:
        print("1. Add Expense")
        print("2. Change Monthly Budget")
        print("3. View Expense Summary")
        print("4. View Expense Summary By Category")
        print("5. Load Previous Summaries")
        print("6. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            print()
            expense = expense_input()
            expense_to_file(expense, finance_file)
            print()
        elif choice == '2':
            budget = manage_budget(budget_file)
        elif choice == '3':
            expense_summary(finance_file, budget)
        elif choice == '4':
            expense_summary_category(finance_file, budget)
        elif choice == '5':
            load_previous_summaries()
        elif choice == '6':
            break
        else:
            print("Choose a valid option.")

def monthly_save(finance_file):
    today = date.today()
    month_year = today.strftime("%B_%Y")
    save_file = f"expenses_{month_year}.csv"
    if os.path.exists(finance_file):
        os.rename(finance_file, save_file)

def save_list():
    monthly_summaries = [x for x in os.listdir() if x.startswith("expenses") and x.endswith(".csv")]
    return monthly_summaries

def load_previous_summaries():
    summaries = save_list()
    if not summaries:
        print()
        print("No available summaries.")
        return []
    print()
    print("Avaialble Summaries:")
    for i, summary in enumerate(summaries, 1):
        print(f"{i}. {summary.replace('expenses_', '').replace('.csv', '')}")
    while True:
        try:
            choice = int(input("Enter the number of the summary to view: "))
            if 1 <= choice <= len(summaries):
                selected_summary = summaries[choice -1]
                expense_summary(selected_summary, load_budget("budget.txt"))
                break
            else:
                print("Invalid option.")
        except ValueError:
            print("Enter a number.")

def check_reset_date(finance_file):
    latest_file = "latest_file.txt"
    today = date.today()
    current_date = today.isoformat()

    if os.path.exists(latest_file):
        with open(latest_file, "r") as f:
            last_date_str = f.read().strip()
            try:
                last_date = datetime.fromisoformat(last_date_str).date()
            except ValueError:
                last_date = today

            if last_date.month != today.month or last_date.year != today.year:
                if os.path.exists(finance_file):
                    monthly_save(finance_file)
                with open(finance_file, "w") as f:
                    f.write("")
    else:
        with open(finance_file, "w") as f:
            f.write("")
    
    with open(latest_file, "w") as f:
        f.write(current_date)
            
def load_budget(budget_file):
    if os.path.exists(budget_file):
        with open(budget_file, "r") as f:
            return float(f.read().strip())
    return 0

def save_budget(budget, budget_file):
    with open(budget_file, "w") as f:
        f.write(str(budget))

def manage_budget(budget_file):
    budget = load_budget(budget_file)
    print()
    print(f"Current Budget: ${budget:.2f}")
    new_budget = float(input("Enter your budget: "))
    save_budget(new_budget, budget_file)

    print("Would you like to split/change budget among any of the categories? (Yes/No)")
    split_option = input().strip()

    if split_option == 'Yes':
        expense_categories = {1: "Groceries", 2: "Rent", 3: "Utilities", 4: "Investments", 5: "Eating Out", 6: "Transportation", 7: "Fun",  8: "Misc"}
        category_budgets = {}
        total_percentage = 0
        for index, category in expense_categories.items():
            while True:
                try:
                    percentage = float(input(f"Enter percentage for {category} [0-100]: "))
                    if 0 <= percentage <= 100:
                        category_budgets[category] = new_budget * (percentage / 100)
                        total_percentage += percentage
                        break
                    else:
                        print("Invalid percentage.")
                except ValueError:
                    print("Invalid input. Use a valid number.")

        if total_percentage > 100:
            print("Total percentage is over  100%")
            return manage_budget(budget_file)
        save_percentages(category_budgets)
    else:
        save_percentages({})
    print(f"New Monthly Budget: ${new_budget:.2f}")
    print()
    return new_budget


def quicksort(expenses):
    if len(expenses) <= 1:
        return expenses
    else:
        pivot = expenses[len(expenses) //2].cost
        left = [x for x in expenses if x.cost > pivot]
        middle = [x for x in expenses if x.cost == pivot]
        right = [x for x in expenses if x.cost < pivot]
        return quicksort(left) + middle + quicksort(right)
    
def save_percentages(category_budgets):
    with open("category_budgets.txt", "w") as f:
        for category, budget in category_budgets.items():
            f.write(f"{category}, {budget:.2f}\n")

def expense_input():
    print(f"Expense Input")
    expense_item = input("Enter exepnse: ")
    while True:
        try:
            expense_cost = float(input("Enter expense cost: "))
            break
        except ValueError:
            print("Invalid input, enter a value.")

    expense_categories = {1: "Groceries", 2: "Rent", 3: "Utilities", 4: "Investments", 
                          5: "Eating Out", 6: "Transportation", 7: "Fun",  8: "Misc"}

    while True:
        print()
        print("Category of Spending: ")
        for index, category in expense_categories.items():
            print(f" {index}: {category}")

        value_range = f"[1 - {len(expense_categories)}]"
        try:
            selected_index = int(input(f"Category number {value_range}: "))
        

            if selected_index in expense_categories:
                selected_category = expense_categories[selected_index]
                print()
                print(f"Selected category: {selected_category}")
                today = date.today()
                visual_date = today.strftime('%d-%m-%Y')
                new_expense = Expense(name=expense_item, type = selected_category, cost = expense_cost, date=visual_date)
                return new_expense
            
            else:
                print("Unknown index, try again.")
        except ValueError:
            print("Enter a number.")

def save_percentages(category_budgets):
    with open("category_budgets.txt", "w") as f:
        for category, budget in category_budgets.items():
            f.write(f"{category}, {budget:.2f}\n")

def expense_to_file(expense, finance_file):
    today = date.today()
    visual_date = today.strftime('%d-%m-%Y')
    print(f"Saving Expense: {expense}")
    with open(finance_file, "a") as f:
        formatted = f"| {expense.name}, {expense.type}, ${expense.cost:.2f}, {visual_date} | \n"
        f.write(formatted)

def expense_summary(finance_file, budget):
    print()
    print(f"Expense Summary:")
    expenses = []
    total_spent = 0
    with open(finance_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().strip('|').split(", ")
            if len(parts) == 4:
                name, category, cost, date = parts
                cost = float(cost.replace("$", "").replace(",", ""))
                expenses.append(Expense(name, category, cost, date))
                total_spent += cost
    sorted = quicksort(expenses)
    for expense in sorted:
        print(f"| {expense.name}, {expense.type}, ${expense.cost:.2f}, {expense.date} |")
    print()
    print(f"Money Spent This Month: ${total_spent:.2f}")
    remaining_budget = budget - total_spent
    print(f"Budget Remaining: ${remaining_budget:.2f}")
    print()

def expense_summary_category(finance_file, budget):
    print()
    print("Expense Summary by Category")

    category_budgets = load_category_budgets()
    total_by_category = defaultdict(float)
    total_spent = 0

    with open(finance_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().strip('|').split(", ")
            if len(parts) == 4:
                name, category, amount, date = parts
                try:
                    amount = float(amount.replace("$", "").replace(",", ""))
                except ValueError:
                    print(f"Error.")
                    continue
                total_by_category[category] += amount
                total_spent += amount

    categories = list(total_by_category.keys())
    spending = list(total_by_category.values())
    allotted_budget = [category_budgets.get(x, 0) for x in categories]

    for category, total in total_by_category.items():
        if category in category_budgets:
            allotted_budget = category_budgets[category]
            if allotted_budget > 0:
                split_percentage = (allotted_budget / budget) * 100
                revised_budget = allotted_budget - total
                print()
                print(f"-{category}: ${total:.2f}")
                print(f" Allotted Budget: ${allotted_budget:.2f} ({split_percentage:.2f}%)")
                print(f" Remaining Budget: ${revised_budget:.2f}")
            else:
                print()
                print(f"-{category}: ${total:.2f}")
        else:
            print()
            print(f"-{category}: ${total:.2f}")

    print()
    print(f"Money Spent This Month: ${total_spent:.2f}")
    remaining_budget = budget - total_spent
    print(f"Budget Remaining This Month: ${remaining_budget:.2f}")
    print()

    print("Visualize spending by category with a graph?")
    choice = input("(Yes/No): ")
    if choice == "Yes":
        plt.figure(figsize=(8, 5))
        plt.pie(spending, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title('Expense Summary By Category')
        plt.show()
        plt.figure(figsize=(8, 5))
        bar_width = 0.30
        index = range(len(categories))

        plt.bar(index, spending, bar_width, label='Spent')
        plt.bar([x + bar_width for x in index], allotted_budget, bar_width, label='Alloted Budget')
    
        plt.xlabel('Category')
        plt.ylabel('Amount ($)')
        plt.title('Expense Summary By Category')
        plt.xticks([x + bar_width / 2 for x in index], categories, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout
        plt.show()


def load_category_budgets():
    category_budgets = {}
    if os.path.exists("category_budgets.txt"):
        with open("category_budgets.txt", "r") as f:
            for line in f:
                parts = line.strip().split(", ")
                if len(parts) == 2:
                    category, budget = parts
                    try:
                        category_budgets[category] = float(budget)
                    except ValueError:
                        print(f"Error.")
    return category_budgets

if __name__ == "__main__":
    main()
