import pandas as pd
import os
import html

def check_and_fix_csv(file_path, required_columns, column_to_escape):
    print(f"Checking file: {file_path}")
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    try:
        # Load the CSV file
        data = pd.read_csv(file_path, delimiter=";")

        # Check for missing required columns
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            print(f"❌ Missing columns in {file_path}: {missing_columns}")
            return

        print(f"✅ All expected columns are present.")

        # Escape HTML in the specified column
        if column_to_escape in data.columns:
            original_html_values = data[column_to_escape].dropna().unique()[:5]
            data[column_to_escape] = data[column_to_escape].apply(
                lambda x: html.escape(str(x)) if pd.notnull(x) else x
            )
            escaped_html_values = data[column_to_escape].dropna().unique()[:5]

            print("🔍 Example HTML values before escaping:")
            print(original_html_values)
            print("🔍 Example HTML values after escaping:")
            print(escaped_html_values)

        # Check for missing values
        empty_values = data.isnull().sum().sum()
        print(f"Number of empty values: {empty_values}")

        # Check for inconsistent rows
        inconsistent_rows = data[data.isnull().any(axis=1)]
        if not inconsistent_rows.empty:
            print(f"❌ Inconsistent rows detected: {len(inconsistent_rows)}")
            print("Example inconsistent rows:")
            print(inconsistent_rows.head())

        # Save the sanitized data
        sanitized_file = file_path.replace(".csv", "_sanitized.csv")
        data.to_csv(sanitized_file, index=False, sep=";")
        print(f"✅ Sanitized file saved as: {sanitized_file}")

    except Exception as e:
        print(f"❌ Error processing file {file_path}: {e}")

# Configuration for categories_description.csv
file_path = "./csv_files/categories_description.csv"
required_columns = [
    "categories_id",
    "language_id",
    "categories_name",
    "categories_heading_title",
    "categories_description",
]
column_to_escape = "categories_description"

# Run the checker
check_and_fix_csv(file_path, required_columns, column_to_escape)