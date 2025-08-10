"""
db.py — SQLite data layer for FinTrack Pro (Stage 3)

Creates and manages:
 - expenses table (id, date, amount, category, description)
 - budgets table (category -> limit_amount)
 - overall_budget table (single-row overall monthly budget)

All functions are small and return primitive types (lists/tuples/floats)
so GUI and utils can call them without dealing with SQL directly.
"""

import sqlite3
from datetime import datetime

DB_NAME = "expenses.db"


# -------------------------
# Low-level helpers
# -------------------------
def _connect():
    return sqlite3.connect(DB_NAME)


# -------------------------
# Initialization
# -------------------------
def init_db():
    """Create DB and tables if they don't exist."""
    conn = _connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        category TEXT PRIMARY KEY,
        limit_amount REAL NOT NULL
    )
    """)

    # single-row table to store overall monthly budget
    cur.execute("""
    CREATE TABLE IF NOT EXISTS overall_budget (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        limit_amount REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# -------------------------
# Expense operations
# -------------------------
def add_expense(date, amount, category, description):
    """Insert a new expense."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)",
        (date, amount, category, description)
    )
    conn.commit()
    conn.close()


def get_all_expenses():
    """
    Return list of expenses as tuples:
    (id INTEGER, date TEXT, amount REAL, category TEXT, description TEXT)
    Ordered by date DESC, id DESC.
    """
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT id, date, amount, category, description FROM expenses ORDER BY date DESC, id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_expense_by_id(expense_id):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT id, date, amount, category, description FROM expenses WHERE id = ?", (expense_id,))
    row = cur.fetchone()
    conn.close()
    return row


def update_expense(expense_id, date, amount, category, description):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
        UPDATE expenses
        SET date = ?, amount = ?, category = ?, description = ?
        WHERE id = ?
    """, (date, amount, category, description, expense_id))
    conn.commit()
    conn.close()


def delete_expense(expense_id):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


# -------------------------
# Budget operations
# -------------------------
def set_budget(category, limit_amount):
    """
    Set or update a category budget. `category` is a string.
    Use a special category name (e.g. '__total__') only if you want, but
    we store the overall budget in the overall_budget table instead.
    """
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO budgets (category, limit_amount)
        VALUES (?, ?)
        ON CONFLICT(category) DO UPDATE SET limit_amount = excluded.limit_amount
    """, (category, limit_amount))
    conn.commit()
    conn.close()


def get_budget(category):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT limit_amount FROM budgets WHERE category = ?", (category,))
    row = cur.fetchone()
    conn.close()
    return float(row[0]) if row else None


def delete_budget(category):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM budgets WHERE category = ?", (category,))
    conn.commit()
    conn.close()


def get_all_budgets():
    """Return list of (category, limit_amount)."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT category, limit_amount FROM budgets")
    rows = cur.fetchall()
    conn.close()
    return rows


# -------------------------
# Overall monthly budget
# -------------------------
def set_overall_budget(limit_amount):
    """Insert or update the single overall budget row (id = 1)."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO overall_budget (id, limit_amount) VALUES (1, ?)
        ON CONFLICT(id) DO UPDATE SET limit_amount = excluded.limit_amount
    """, (limit_amount,))
    conn.commit()
    conn.close()


def get_overall_budget():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT limit_amount FROM overall_budget WHERE id = 1")
    row = cur.fetchone()
    conn.close()
    return float(row[0]) if row else None


# -------------------------
# Monthly aggregation helpers
# -------------------------
def _month_prefix_for(date_obj=None):
    # returns string like "2025-08"
    if date_obj is None:
        date_obj = datetime.now()
    return date_obj.strftime("%Y-%m")


def get_total_spent_for_month(month_prefix=None):
    """Sum of amount for given month_prefix (YYYY-MM). Defaults to current month."""
    if month_prefix is None:
        month_prefix = _month_prefix_for()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date LIKE ?", (month_prefix + "%",))
    val = cur.fetchone()[0] or 0.0
    conn.close()
    return float(val)


def get_category_spent_for_month(category, month_prefix=None):
    if month_prefix is None:
        month_prefix = _month_prefix_for()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE category = ? AND date LIKE ?", (category, month_prefix + "%"))
    val = cur.fetchone()[0] or 0.0
    conn.close()
    return float(val)

def edit_expense(expense_id, date, amount, category, description):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute('''
        UPDATE expenses
        SET date = ?, amount = ?, category = ?, description = ?
        WHERE id = ?
    ''', (date, amount, category, description, expense_id))
    conn.commit()
    conn.close()