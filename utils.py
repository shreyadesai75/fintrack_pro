"""
utils.py — Shared helpers for FinTrack Pro (Stage 3)
Uses db.py for all persistence; contains validation, formatting, and budget checking logic.
"""

from datetime import datetime
from tkinter import messagebox
import db


# -------------------------
# Date validation
# -------------------------
def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter the date in YYYY-MM-DD format.")
        return False

import json
import os

EXPENSES_FILE = "expenses.json"

# Load expenses from JSON file (CLI Stage 1/2)
def load_expenses():
    if not os.path.exists(EXPENSES_FILE):
        return []
    with open(EXPENSES_FILE, "r") as f:
        return json.load(f)

# Save expenses list to JSON file
def save_expenses(expenses):
    with open(EXPENSES_FILE, "w") as f:
        json.dump(expenses, f, indent=2)

# CLI add expense function
def add_expense(expenses):
    print("Add New Expense")
    date = input("Date (YYYY-MM-DD): ")
    amount = input("Amount: ")
    category = input("Category: ")
    description = input("Description: ")
    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount!")
        return
    new_id = max([e["id"] for e in expenses], default=0) + 1
    expenses.append({
        "id": new_id,
        "date": date,
        "amount": amount,
        "category": category,
        "description": description
    })
    print("Expense added.")

# CLI view expenses function
def view_expenses(expenses):
    print("\nYour Expenses:")
    if not expenses:
        print("No expenses found.")
        return
    for e in expenses:
        print(f'ID: {e["id"]}, Date: {e["date"]}, Amount: {e["amount"]}, Category: {e["category"]}, Desc: {e["description"]}')

# CLI edit expense function
def edit_expense(expenses):
    try:
        eid = int(input("Enter expense ID to edit: "))
    except ValueError:
        print("Invalid ID")
        return
    for e in expenses:
        if e["id"] == eid:
            date = input(f"Date [{e['date']}]: ") or e['date']
            amount = input(f"Amount [{e['amount']}]: ") or str(e['amount'])
            category = input(f"Category [{e['category']}]: ") or e['category']
            description = input(f"Description [{e['description']}]: ") or e['description']
            try:
                amount = float(amount)
            except ValueError:
                print("Invalid amount!")
                return
            e.update({
                "date": date,
                "amount": amount,
                "category": category,
                "description": description
            })
            print("Expense updated.")
            return
    print("Expense ID not found.")

# CLI delete expense function
def delete_expense(expenses):
    try:
        eid = int(input("Enter expense ID to delete: "))
    except ValueError:
        print("Invalid ID")
        return
    for i, e in enumerate(expenses):
        if e["id"] == eid:
            del expenses[i]
            print("Expense deleted.")
            return
    print("Expense ID not found.")

# -------------------------
# Amount validation
# -------------------------
def validate_amount(amount_text):
    try:
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError
        return True
    except ValueError:
        messagebox.showerror("Invalid Amount", "Please enter a valid positive number for amount.")
        return False


# -------------------------
# Load expenses from DB
# -------------------------
def load_expenses():
    return db.get_all_expenses()


# -------------------------
# Budget check logic
# -------------------------
def check_budget(category, new_amount):
    """
    Check if adding `new_amount` to current month total/category would exceed budgets.
    Shows messagebox warnings if needed.
    """
    # Total budget
    total_budget = db.get_overall_budget()
    if total_budget is not None:
        total_spent = db.get_total_spent_for_month()
        if total_spent + new_amount > total_budget:
            messagebox.showwarning(
                "Budget Exceeded",
                f"Adding this expense will exceed your monthly total budget of {format_currency(total_budget)}!\n"
                f"Current total: {format_currency(total_spent)}"
            )

    # Category budget
    category_budget = db.get_budget(category)
    if category_budget is not None:
        category_spent = db.get_category_spent_for_month(category)
        if category_spent + new_amount > category_budget:
            messagebox.showwarning(
                "Category Budget Exceeded",
                f"Adding this expense will exceed your budget for {category} ({format_currency(category_budget)}).\n"
                f"Current category total: {format_currency(category_spent)}"
            )


# -------------------------
# Formatting helpers
# -------------------------
def format_currency(amount):
    """Return amount as string with 2 decimal places."""
    return f"{amount:.2f}"


# -------------------------
# Date helper
# -------------------------
def today_str():
    """Return today's date as YYYY-MM-DD string."""
    return datetime.now().strftime("%Y-%m-%d")
