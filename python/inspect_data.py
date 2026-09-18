from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def inspect_dataset(file_path):
    """Inspect one CSV dataset and print a data-quality summary."""

    print("\n" + "=" * 80)
    print(f"DATASET: {file_path.name}")
    print("=" * 80)

    df = pd.read_csv(file_path)

    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumns:")
    print(list(df.columns))

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)

    missing_report = pd.DataFrame({
        "missing_count": missing,
        "missing_percentage": missing_pct
    })

    print(missing_report[missing_report["missing_count"] > 0])

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nFirst 3 Rows:")
    print(df.head(3).to_string(index=False))


def main():
    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in: {RAW_DATA_DIR}")
        return

    print(f"Found {len(csv_files)} CSV files.")

    for file_path in csv_files:
        try:
            inspect_dataset(file_path)
        except Exception as error:
            print(f"\nERROR reading {file_path.name}:")
            print(error)


if __name__ == "__main__":
    main()