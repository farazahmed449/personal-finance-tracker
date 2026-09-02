# Personal Finance Tracker

A simple personal finance tracker built with Python. It allows users to record income and expenses, view transactions within a date range, calculate financial summaries, and visualize spending and income trends.

## Features

* Add income and expense transactions
* Store transactions in a CSV file
* Filter transactions by date range
* Calculate:

  * Total income
  * Total expenses
  * Net savings
* View income and expense trends
* View expense breakdown by description
* Web interface using Streamlit
* Command-line interface

## Technologies Used

* Python
* Pandas
* Streamlit
* Matplotlib
* Plotly
* CSV
* Git & GitHub

## Project Structure

```text
personal_finance_tracker/
│
├── main.py
├── app.py
├── data_entry.py
├── README.md
├── .gitignore
└── finance_data.csv
```

> `finance_data.csv` is ignored by Git because it contains personal financial data.

## How to Run

### 1. Activate the virtual environment

```powershell
.venv\Scripts\activate
```

### 2. Run the Streamlit application

```powershell
streamlit run app.py
```

The application will open in your browser.

## Command-Line Version

You can also run the backend command-line application:

```powershell
python main.py
```

## Usage

### Add a Transaction

Enter:

* Transaction date
* Amount
* Category
* Description

The transaction is then saved to the local CSV file.

### Dashboard

The dashboard allows you to:

1. Select a date range
2. View transactions
3. View total income
4. View total expenses
5. View net savings
6. View income vs. expense trends
7. View an expense breakdown

## Data Storage

Transactions are stored locally in:

```text
finance_data.csv
```

The file is intentionally excluded from Git using `.gitignore` so personal financial information is not uploaded to GitHub.

## Learning Project

This project was built as a learning project to practice:

* Python fundamentals
* Functions
* Classes and OOP
* File handling
* CSV data
* Pandas
* Data filtering and aggregation
* Data visualization
* Streamlit
* Git and GitHub
