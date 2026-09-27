import argparse
import sys

from expense_analyzer import (
    ExpenseDataError,
    load_expenses,
    category_totals,
    monthly_totals,
    save_category_chart,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize expenses from a CSV file.")
    parser.add_argument(
        "csv_path",
        nargs="?",
        default="expenses.csv",
        help="Path to the expenses CSV file (default: expenses.csv)",
    )
    parser.add_argument(
        "--chart",
        action="store_true",
        help="Save a bar chart of expenses by category to expenses_chart.png",
    )
    args = parser.parse_args()

    try:
        df = load_expenses(args.csv_path)
    except ExpenseDataError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    totals = category_totals(df)

    print("Expenses by category:\n")
    for category, amount in totals.items():
        print(f"{category:<15} {amount:>10.2f}")

    print(f"\nTotal: {totals.sum():.2f}")

    monthly = monthly_totals(df)
    if monthly is not None:
        print("\nMonthly breakdown:\n")
        print(monthly.round(2).to_string())
    else:
        print("\nNo usable Date column found - skipping monthly breakdown.")

    if args.chart:
        chart_path = "expenses_chart.png"
        save_category_chart(totals, chart_path)
        print(f"\nChart saved to {chart_path}")


if __name__ == "__main__":
    main()
