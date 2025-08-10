import tkinter as tk
from tkinter import ttk, messagebox
from utils import validate_date, validate_amount, check_budget, load_expenses
import db
import tkinter as tk
from tkinter import messagebox
import ml.predictor as ml_predictor
# -------------------------
# GUI Logic
# -------------------------
def refresh_table(tree):
    """Reload the table data from the database."""
    for row in tree.get_children():
        tree.delete(row)
    for expense in load_expenses():
        # expense is tuple: (id, date, amount, category, description)
        tree.insert("", "end", values=expense)

def add_expense_window(parent, tree):
    """Popup window to add a new expense."""
    win = tk.Toplevel(parent)
    win.title("Add Expense")

    tk.Label(win, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
    date_entry = tk.Entry(win)
    date_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(win, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
    amount_entry = tk.Entry(win)
    amount_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(win, text="Category:").grid(row=2, column=0, padx=5, pady=5)
    category_entry = tk.Entry(win)
    category_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(win, text="Description:").grid(row=3, column=0, padx=5, pady=5)
    description_entry = tk.Entry(win)
    description_entry.grid(row=3, column=1, padx=5, pady=5)

    import ml.predictor as ml_predictor  # Add this import at the top of gui.py

def add_expense_window(parent, tree):
    """Popup window to add a new expense."""
    win = tk.Toplevel(parent)
    win.title("Add Expense")

    tk.Label(win, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
    date_entry = tk.Entry(win)
    date_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(win, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
    amount_entry = tk.Entry(win)
    amount_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(win, text="Category:").grid(row=2, column=0, padx=5, pady=5)
    category_entry = tk.Entry(win)
    category_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(win, text="Description:").grid(row=3, column=0, padx=5, pady=5)
    description_entry = tk.Entry(win)
    description_entry.grid(row=3, column=1, padx=5, pady=5)

    def suggest_category():
        desc = description_entry.get()
        if not desc.strip():
            messagebox.showinfo("Info", "Please enter a description first!")
            return
        try:
            suggested = ml_predictor.suggest_category(desc)
            category_entry.delete(0, tk.END)
            category_entry.insert(0, suggested)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to predict category:\n{e}")

    # Add Suggest Category button
    suggest_btn = tk.Button(win, text="Suggest Category", command=suggest_category)
    suggest_btn.grid(row=2, column=2, padx=5, pady=5)

    def save_new():
        date = date_entry.get()
        amount_text = amount_entry.get()
        category = category_entry.get()
        description = description_entry.get()

        if not (validate_date(date) and validate_amount(amount_text)):
            return

        amount = float(amount_text)
        check_budget(category, amount)

        db.add_expense(date, amount, category, description)
        refresh_table(tree)
        win.destroy()

    tk.Button(win, text="Save", command=save_new).grid(row=4, column=0, columnspan=3, pady=10)

    def suggest_category():
        desc = description_entry.get()
        if not desc.strip():
            messagebox.showinfo("Info", "Please enter a description first!")
            return
        try:
            suggested = ml_predictor.suggest_category(desc)
            category_entry.delete(0, tk.END)
            category_entry.insert(0, suggested)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to predict category:\n{e}")

    # Add Suggest Category button
    suggest_btn = tk.Button(win, text="Suggest Category", command=suggest_category)
    suggest_btn.grid(row=2, column=2, padx=5, pady=5)

    def save_new():
        date = date_entry.get()
        amount_text = amount_entry.get()
        category = category_entry.get()
        description = description_entry.get()

        if not (validate_date(date) and validate_amount(amount_text)):
            return

        amount = float(amount_text)
        check_budget(category, amount)

        db.add_expense(date, amount, category, description)
        refresh_table(tree)
        win.destroy()

    tk.Button(win, text="Save", command=save_new).grid(row=4, column=0, columnspan=3, pady=10)
    def save_new():
        date = date_entry.get()
        amount_text = amount_entry.get()
        category = category_entry.get()
        description = description_entry.get()

        if not (validate_date(date) and validate_amount(amount_text)):
            return

        amount = float(amount_text)
        check_budget(category, amount)

        db.add_expense(date, amount, category, description)
        refresh_table(tree)
        win.destroy()

    tk.Button(win, text="Save", command=save_new).grid(row=4, column=0, columnspan=2, pady=10)

def edit_expense_window(parent, tree):
    """Popup window to edit selected expense."""
    selected = tree.selection()
    if not selected:
        messagebox.showerror("No Selection", "Please select an expense to edit.")
        return
    expense = tree.item(selected[0], "values")

    win = tk.Toplevel(parent)
    win.title("Edit Expense")

    tk.Label(win, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
    date_entry = tk.Entry(win)
    date_entry.insert(0, expense[1])
    date_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(win, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
    amount_entry = tk.Entry(win)
    amount_entry.insert(0, expense[2])
    amount_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(win, text="Category:").grid(row=2, column=0, padx=5, pady=5)
    category_entry = tk.Entry(win)
    category_entry.insert(0, expense[3])
    category_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(win, text="Description:").grid(row=3, column=0, padx=5, pady=5)
    description_entry = tk.Entry(win)
    description_entry.insert(0, expense[4])
    description_entry.grid(row=3, column=1, padx=5, pady=5)

    def save_edit():
        date = date_entry.get()
        amount_text = amount_entry.get()
        category = category_entry.get()
        description = description_entry.get()

        if not (validate_date(date) and validate_amount(amount_text)):
            return

        amount = float(amount_text)
        check_budget(category, amount)

        db.edit_expense(expense[0], date, amount, category, description)
        refresh_table(tree)
        win.destroy()

    tk.Button(win, text="Save Changes", command=save_edit).grid(row=4, column=0, columnspan=2, pady=10)

def delete_selected(tree):
    """Delete the selected expense."""
    selected = tree.selection()
    if not selected:
        messagebox.showerror("No Selection", "Please select an expense to delete.")
        return
    expense = tree.item(selected[0], "values")
    confirm = messagebox.askyesno("Delete", f"Delete expense ID {expense[0]}?")
    if confirm:
        db.delete_expense(expense[0])
        refresh_table(tree)

def set_budget_window(parent):
    """Popup window to set a category or total budget."""
    win = tk.Toplevel(parent)
    win.title("Set Budget")

    tk.Label(win, text="Category (leave blank for total):").grid(row=0, column=0, padx=5, pady=5)
    category_entry = tk.Entry(win)
    category_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(win, text="Limit Amount:").grid(row=1, column=0, padx=5, pady=5)
    amount_entry = tk.Entry(win)
    amount_entry.grid(row=1, column=1, padx=5, pady=5)

    def save_budget():
        category = category_entry.get().strip()
        try:
            amount = float(amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid number.")
            return

        if category:
            db.set_budget(category, amount)
        else:
            db.set_overall_budget(amount)

        messagebox.showinfo("Success", "Budget set successfully.")
        win.destroy()

    tk.Button(win, text="Save", command=save_budget).grid(row=2, column=0, columnspan=2, pady=10)
try:
    from ml.predictor import suggest_category
except ImportError:
    suggest_category = None  # fallback if ML not ready

class ExpenseForm(tk.Toplevel):
    def __init__(self, parent, save_callback, initial_data=None):
        super().__init__(parent)
        self.title("Expense Form")

        tk.Label(self, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(self)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Category:").grid(row=2, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(self)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Description:").grid(row=3, column=0, padx=5, pady=5)
        self.description_entry = tk.Entry(self)
        self.description_entry.grid(row=3, column=1, padx=5, pady=5)

        # Bind focus out event to suggest category
        self.description_entry.bind("<FocusOut>", self.on_description_focus_out)

        # If editing, pre-fill data
        if initial_data:
            self.date_entry.insert(0, initial_data.get('date', ''))
            self.amount_entry.insert(0, initial_data.get('amount', ''))
            self.category_entry.insert(0, initial_data.get('category', ''))
            self.description_entry.insert(0, initial_data.get('description', ''))

        tk.Button(self, text="Save", command=self.save).grid(row=4, column=0, columnspan=2, pady=10)

        self.save_callback = save_callback

    def on_description_focus_out(self, event=None):
        if suggest_category is None:
            return
        desc = self.description_entry.get().strip()
        if desc:
            try:
                prediction = suggest_category(desc)
                current_cat = self.category_entry.get().strip()
                if not current_cat or current_cat.lower() != prediction.lower():
                    self.category_entry.delete(0, tk.END)
                    self.category_entry.insert(0, prediction)
            except Exception as e:
                print(f"Category suggestion error: {e}")

    def save(self):
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()

        # You can add your validation here or pass to callback
        self.save_callback(date, amount, category, description)
        self.destroy()
def run_app():
    db.init_db()

    root = tk.Tk()
    root.title("FinTrack Pro")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    columns = ("ID", "Date", "Amount", "Category", "Description")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack()

    refresh_table(tree)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Add Expense", command=lambda: add_expense_window(root, tree)).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Edit Selected", command=lambda: edit_expense_window(root, tree)).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Delete Selected", command=lambda: delete_selected(tree)).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Set Budget", command=lambda: set_budget_window(root)).grid(row=0, column=3, padx=5)
    tk.Button(btn_frame, text="Refresh", command=lambda: refresh_table(tree)).grid(row=0, column=4, padx=5)

    root.mainloop()

if __name__ == "__main__":
    run_app()
