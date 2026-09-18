from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
REPORT_DIR = PROJECT_ROOT / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


def profile_dataset(file_path):
    """Generate a data-quality profile for one CSV file."""

    df = pd.read_csv(file_path)

    total_rows = len(df)

    report = []

    for column in df.columns:
        missing_count = int(df[column].isna().sum())
        duplicate_count = int(df[column].duplicated().sum())

        report.append({
            "dataset": file_path.name,
            "column": column,
            "data_type": str(df[column].dtype),
            "row_count": total_rows,
            "missing_count": missing_count,
            "missing_percentage": round(
                (missing_count / total_rows) * 100, 2
            ),
            "unique_values": int(df[column].nunique(dropna=True)),
            "duplicate_values": duplicate_count,
        })

    return report


def main():
    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in: {RAW_DATA_DIR}")
        return

    print(f"Found {len(csv_files)} CSV files.")

    all_reports = []

    for file_path in csv_files:
        print(f"Profiling: {file_path.name}")

        try:
            dataset_report = profile_dataset(file_path)
            all_reports.extend(dataset_report)

        except Exception as error:
            print(f"ERROR: {error}")

    report_df = pd.DataFrame(all_reports)

    output_file = REPORT_DIR / "data_quality_report.csv"

    report_df.to_csv(output_file, index=False)

    print("\n" + "=" * 70)
    print("DATA QUALITY REPORT CREATED")
    print("=" * 70)
    print(f"File: {output_file}")
    print(f"Columns profiled: {len(report_df)}")

    print("\nColumns with missing values:")

    missing = report_df[
        report_df["missing_count"] > 0
    ][
        [
            "dataset",
            "column",
            "missing_count",
            "missing_percentage"
        ]
    ]

    if missing.empty:
        print("No missing values found.")
    else:
        print(missing.to_string(index=False))


if __name__ == "__main__":
    main()