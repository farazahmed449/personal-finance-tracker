"""
Personal Finance Tracker - Streamlit Frontend

This module provides the web interface for:
- Adding income and expense transactions
- Viewing transactions within a date range
- Displaying financial summaries
- Visualizing income and expenses
- Showing expense breakdowns
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from main import CSV

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide"
)


# ==================================================
# INITIALIZE
# ==================================================

CSV.initialize_csv()

st.title("💰 Personal Finance Tracker")
st.caption("Track your income, expenses, and savings in one place.")


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

st.sidebar.title("💰 Finance Tracker")
st.sidebar.caption("Manage your personal finances.")

page = st.sidebar.radio(
    "Navigation",
    ["Add Transaction", "Dashboard"]
)

# ==================================================
# ADD TRANSACTION
# ==================================================

if page == "Add Transaction":

    st.header("➕ Add Transaction")
    st.caption("Record a new income or expense.")

    with st.form("transaction_form"):

        date = st.date_input(
            "Transaction Date"
        )

        amount = st.number_input(
            "Amount",
            min_value=0.01,
            step=0.01
        )

        category = st.selectbox(
            "Category",
            ["Income", "Expense"]
        )

        description = st.text_input(
            "Description"
        )

        submitted = st.form_submit_button(
            "Add Transaction"
        )

        if submitted:

            date = date.strftime(
                CSV.FORMAT
            )

            CSV.add_entries(
                date,
                amount,
                category,
                description
            )

            st.success(
                "Transaction added successfully!"
            )


# ==================================================
# DASHBOARD
# ==================================================

elif page == "Dashboard":

    st.header("📊 Financial Dashboard")
    st.caption("Review your income, expenses, and savings.")

    # ==================================================
    # DATE FILTERS
    # ==================================================

    st.subheader("📅 Select Date Range")
    st.caption("Choose the period you want to analyze.")

    col1, col2 = st.columns(2)

    with col1:

        start_date = st.date_input(
            "Start Date"
        )

    with col2:

        end_date = st.date_input(
            "End Date"
        )

    if st.button("🔍 View Transactions", type="primary"):

        # ==================================================
        # VALIDATE DATE RANGE
        # ==================================================

        if start_date > end_date:

            st.error(
                "Start date cannot be after end date."
            )


        else:


            # ==================================================
            # FORMAT DATES
            # ==================================================

            start_date = start_date.strftime(
                CSV.FORMAT
            )

            end_date = end_date.strftime(
                CSV.FORMAT
            )


            # ==================================================
            # GET TRANSACTIONS
            # ==================================================

            df, total_income, total_expense = CSV.get_transactions(
                start_date,
                end_date
            )


            # ==================================================
            # CHECK FOR EMPTY DATA
            # ==================================================

            if not df.empty:


                # ==================================================
                # FINANCIAL OVERVIEW
                # ==================================================

                st.subheader(
                    "📋 Transaction History"
                )
                st.caption("All transactions within the selected date range.")

                net_savings = (
                    total_income - total_expense
                )


                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "💰 Total Income",
                    f"${total_income:,.2f}",
                    help="Total income during the selected date range."
                )

                col2.metric(
                    "💸 Total Expense",
                    f"${total_expense:,.2f}",
                    help="Total expenses during the selected date range."
                )

                col3.metric(
                    "📈 Net Savings",
                    f"${net_savings:,.2f}",
                    help="Income minus expenses during the selected date range."
                )


                # ==================================================
                # INCOME VS EXPENSES
                # ==================================================

                st.subheader(
                    "📈 Income vs Expenses"
                )

                plot_df = df.copy()

                plot_df["date"] = pd.to_datetime(
                    plot_df["date"]
                )

                plot_df = plot_df.set_index(
                    "date"
                )


                income_df = (
                    plot_df[
                        plot_df["category"] == "Income"
                    ]["amount"]
                    .resample("D")
                    .sum()
                )


                expense_df = (
                    plot_df[
                        plot_df["category"] == "Expense"
                    ]["amount"]
                    .resample("D")
                    .sum()
                )


                fig, ax = plt.subplots(
                    figsize=(10, 5)
                )


                ax.plot(
                    income_df.index,
                    income_df,
                    label="Income"
                )

                ax.plot(
                    expense_df.index,
                    expense_df,
                    label="Expense"
                )


                ax.set_xlabel("Date")

                ax.set_ylabel("Amount")

                ax.set_title(
                    "Income vs Expenses Over Time"
                )

                ax.legend()

                ax.grid(True)


                st.pyplot(fig)


                # ==================================================
                # EXPENSE BREAKDOWN
                # ==================================================

                st.subheader(
                    "📊 Expense Breakdown"
                )
                st.caption("See where your money is being spent.")


                expense_data = df[
                    df["category"] == "Expense"
                ]


                if not expense_data.empty:

                    expense_by_category = (
                        expense_data
                        .groupby("desc")["amount"]
                        .sum()
                        .sort_values()
                        .reset_index()
                    )


                    fig2 = px.bar(
                        expense_by_category,
                        x="amount",
                        y="desc",
                        orientation="h",
                        title="Expenses by Category",
                        labels={
                            "amount": "Amount",
                            "desc": "Category"
                        }
                    )


                    fig2.update_layout(
                        height=450
                    )


                    st.plotly_chart(
                        fig2,
                        use_container_width=True
                    )


                else:

                    st.info(
                        "No expenses found for this date range."
                    )


                # ==================================================
                # TRANSACTIONS TABLE
                # ==================================================

                st.subheader(
                    "📋 Transactions"
                )


                display_df = df.copy()


                display_df["date"] = (
                    display_df["date"]
                    .dt.strftime("%d-%m-%Y")
                )


                display_df = display_df.rename(
                    columns={
                        "date": "Date",
                        "amount": "Amount",
                        "category": "Category",
                        "desc": "Description"
                    }
                )


                display_df = display_df[
                    [
                        "Date",
                        "Amount",
                        "Category",
                        "Description"
                    ]
                ]


                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )


            # ==================================================
            # NO TRANSACTIONS
            # ==================================================

            else:

                st.info(
                    "📭 No transactions available for the selected date range."
                )