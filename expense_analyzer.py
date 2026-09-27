import pandas as pd

REQUIRED_COLUMNS = {"Category", "Amount"}


class ExpenseDataError(Exception):
    pass


def load_expenses(csv_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise ExpenseDataError(f"File not found: {csv_path}")
    except pd.errors.EmptyDataError:
        raise ExpenseDataError(f"File is empty: {csv_path}")

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ExpenseDataError(
            f"Missing required column(s): {', '.join(sorted(missing))}"
        )

    if df.empty:
        raise ExpenseDataError("No rows found in the file.")

    return df


def category_totals(df: pd.DataFrame) -> pd.Series:
    return df.groupby("Category")["Amount"].sum().sort_values(ascending=False)


def monthly_totals(df: pd.DataFrame) -> pd.DataFrame | None:
    if "Date" not in df.columns:
        return None

    working = df.copy()
    working["Date"] = pd.to_datetime(working["Date"], errors="coerce")
    working = working.dropna(subset=["Date"])

    if working.empty:
        return None

    working["Month"] = working["Date"].dt.to_period("M").astype(str)
    return working.groupby(["Month", "Category"])["Amount"].sum().unstack(fill_value=0)


def save_category_chart(totals: pd.Series, output_path: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5))
    totals.plot(kind="bar", ax=ax, color="#4C72B0")
    ax.set_ylabel("Amount")
    ax.set_title("Expenses by Category")
    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
