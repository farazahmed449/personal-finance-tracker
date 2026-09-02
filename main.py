"""
Personal Finance Tracker - Backend

This module handles:
- Creating and managing the finance CSV file
- Adding income and expense transactions
- Filtering transactions by date
- Calculating income, expenses, and savings
- Displaying transaction trends through a plot
"""

import pandas as pd
import csv
import os
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt


class CSV:
    """Handle storage and retrieval of personal finance transactions."""

    CSV_FILE = os.path.join(
        os.path.dirname(__file__),
        "finance_data.csv"
    )

    COLS = ['date', 'amount', 'category', 'desc']
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        """Create the CSV file with the required columns if it doesn't exist."""
        try:
            pd.read_csv(cls.CSV_FILE)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=cls.COLS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entries(cls, date, amount, category, desc):
        """Add a new income or expense transaction to the CSV file."""
        new_entry = {
            'date': date,
            'amount': amount,
            'category': category,
            'desc': desc
        }

        file_exists = os.path.exists(cls.CSV_FILE)
        file_empty = not file_exists or os.path.getsize(cls.CSV_FILE) == 0

        if file_exists and not file_empty:
            with open(cls.CSV_FILE, "rb") as csv_file:
                csv_file.seek(-1, os.SEEK_END)
                last_char = csv_file.read(1)

            if last_char not in (b"\n", b"\r"):
                with open(cls.CSV_FILE, "a", newline="") as csv_file:
                    csv_file.write("\n")

        with open(cls.CSV_FILE, "a", newline="") as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=cls.COLS
            )

            if file_empty:
                writer.writeheader()

            writer.writerow(new_entry)

        print("Entry Added Successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """Return transactions and financial totals for a date range."""
        df = pd.read_csv(cls.CSV_FILE)

        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No transactions found in the given date range')
            total_income = 0
            total_expense = 0
        else:
            print(
                f"Transactions from "
                f"{start_date.strftime(cls.FORMAT)} to "
                f"{end_date.strftime(cls.FORMAT)}"
            )
            print(filtered_df)

            total_income = filtered_df[
                filtered_df["category"] == "Income"
            ]["amount"].sum()

            total_expense = filtered_df[
                filtered_df["category"] == "Expense"
            ]["amount"].sum()

            print("\nSummary: ")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df, total_income, total_expense


def add():
    """Collect transaction details from the user and save the entry."""
    date = get_date(
        "Enter the date of the Transaction "
        "(dd-mm-yyyy) or enter for today's date: ",
        allow_default=True
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entries(date, amount, category, description)


def plot_transactions(df):
    """Display income and expense trends over time."""
    df = df.copy()
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]["amount"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    expense_df = (
        df[df["category"] == "Expense"]["amount"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df, label="Income", color="g")
    plt.plot(expense_df.index, expense_df, label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    CSV.initialize_csv()

    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            add()

        elif choice == "2":
            start_date = get_date(
                "Enter the start date (dd-mm-yyyy): "
            )
            end_date = get_date(
                "Enter the end date (dd-mm-yyyy): "
            )

            df, total_income, total_expense = CSV.get_transactions(
                start_date,
                end_date
            )

            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)

        elif choice == "3":
            print("Exiting")
            break

        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()