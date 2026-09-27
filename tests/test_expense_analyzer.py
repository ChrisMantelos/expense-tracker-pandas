import pytest

from expense_analyzer import (
    ExpenseDataError,
    load_expenses,
    category_totals,
    monthly_totals,
    save_category_chart,
)


SAMPLE_CSV = """Date,Category,Amount,Description
2026-01-05,Food,25.50,Supermarket
2026-01-06,Transport,10.00,Bus ticket
2026-02-01,Food,15.00,Groceries
2026-02-03,Utilities,60.00,Electricity
"""


def test_load_expenses_missing_file(tmp_path):
    missing = tmp_path / "does_not_exist.csv"
    with pytest.raises(ExpenseDataError):
        load_expenses(str(missing))


def test_load_expenses_missing_columns(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("Foo,Bar\n1,2\n")
    with pytest.raises(ExpenseDataError):
        load_expenses(str(bad_csv))


def test_load_expenses_empty_file(tmp_path):
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("")
    with pytest.raises(ExpenseDataError):
        load_expenses(str(empty_csv))


def test_load_expenses_success(tmp_path):
    csv_path = tmp_path / "expenses.csv"
    csv_path.write_text(SAMPLE_CSV)
    df = load_expenses(str(csv_path))
    assert len(df) == 4
    assert {"Category", "Amount"}.issubset(set(df.columns))


def test_category_totals(tmp_path):
    csv_path = tmp_path / "expenses.csv"
    csv_path.write_text(SAMPLE_CSV)
    df = load_expenses(str(csv_path))
    totals = category_totals(df)

    assert totals["Food"] == pytest.approx(40.50)
    assert totals["Transport"] == pytest.approx(10.00)
    assert totals["Utilities"] == pytest.approx(60.00)
    assert list(totals.index)[0] == "Utilities"


def test_monthly_totals(tmp_path):
    csv_path = tmp_path / "expenses.csv"
    csv_path.write_text(SAMPLE_CSV)
    df = load_expenses(str(csv_path))
    monthly = monthly_totals(df)

    assert monthly is not None
    assert "2026-01" in monthly.index
    assert "2026-02" in monthly.index
    assert monthly.loc["2026-01", "Food"] == pytest.approx(25.50)
    assert monthly.loc["2026-02", "Food"] == pytest.approx(15.00)


def test_monthly_totals_no_date_column(tmp_path):
    csv_path = tmp_path / "expenses.csv"
    csv_path.write_text("Category,Amount\nFood,10\nTransport,5\n")
    df = load_expenses(str(csv_path))
    monthly = monthly_totals(df)
    assert monthly is None


def test_save_category_chart(tmp_path):
    csv_path = tmp_path / "expenses.csv"
    csv_path.write_text(SAMPLE_CSV)
    df = load_expenses(str(csv_path))
    totals = category_totals(df)

    chart_path = tmp_path / "chart.png"
    save_category_chart(totals, str(chart_path))

    assert chart_path.exists()
    assert chart_path.stat().st_size > 0
