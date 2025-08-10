from utils import (
    load_expenses, save_expenses,
    add_expense, view_expenses, edit_expense, delete_expense
)
import db
import gui

def cli_loop():
    expenses = load_expenses()
    while True:
        print("\n==== FinTrack Pro (CLI Mode) ====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)
            save_expenses(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            edit_expense(expenses)
            save_expenses(expenses)
        elif choice == "4":
            delete_expense(expenses)
            save_expenses(expenses)
        elif choice == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

def main():
    print("Welcome to FinTrack Pro!")
    print("Choose mode:")
    print("1. CLI Mode (Stage 1/2)")
    print("2. GUI Mode (Stage 3)")

    mode = input("Enter 1 or 2: ").strip()

    if mode == "1":
        # Run original CLI loop with JSON
        cli_loop()
    elif mode == "2":
        # Init DB and launch GUI
        db.init_db()
        gui.run_app()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
