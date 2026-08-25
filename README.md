# Expense Tracker (Pandas)

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Pandas](https://img.shields.io/badge/data-Pandas-150458)

A small command-line tool that reads a CSV of personal expenses and reports
how much you spent per category. No dashboard, no database - just a fast
way to see where the money went.

## Why I built this

I wanted a five-second answer to "how much did I spend on X this month"
without opening a spreadsheet and building a pivot table every time. This
script does that in one command.

## Example

Given a CSV like:

```
Date,Category,Amount,Description
2026-01-05,Food,25.50,Supermarket
2026-01-06,Transport,10.00,Bus ticket
```

Running the script produces:

```
Expenses by category:

Utilities       95.00
Food            93.45
Entertainment   50.00
Transport       15.00

Total: 253.45
```

## Installation

```bash
git clone https://github.com/ChrisMantelos/expense-tracker-pandas.git
cd expense-tracker-pandas
pip install pandas
```

## Usage

```bash
python main.py
```

By default it reads `expenses.csv` in the project folder. Swap in your own
file with the same column structure and it works the same way.

## CSV format

Required columns: `Category`, `Amount`.
Optional columns (present in the sample file, not required by the script):
`Date`, `Description`.

## How it works

The whole calculation is a single pandas operation:

```python
df.groupby("Category")["Amount"].sum()
```

Everything else in the script is just reading the file, formatting the
output, and printing the total.

## Possible extensions

- Accept the CSV path as a command-line argument instead of a hardcoded filename
- Add a monthly breakdown, not just totals by category
- Add a simple bar chart with matplotlib
- Handle malformed rows instead of failing on them

## Tech stack

Python, Pandas
