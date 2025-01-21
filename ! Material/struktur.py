import pandas as pd
from openpyxl import load_workbook

def extract_template_structure(template_path):
    """
    Extracts column headers from an Excel template file.

    Args:
        template_path (str): Path to the Excel template file.

    Returns:
        list: List of column headers from the template.
    """
    workbook = load_workbook(template_path)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]
    return headers

def transform_data_to_template(data_path, template_path, output_path):
    """
    Transforms the input data to match the structure of the Excel template.

    Args:
        data_path (str): Path to the input data file (CSV or Excel).
        template_path (str): Path to the Excel template file.
        output_path (str): Path to save the transformed Excel file.
    """
    # Extract the template headers
    headers = extract_template_structure(template_path)

    # Load input data
    input_data = pd.read_csv(data_path) if data_path.endswith('.csv') else pd.read_excel(data_path)

    # Create a DataFrame with the template structure
    transformed_data = pd.DataFrame(columns=headers)

    # Match data based on overlapping columns
    common_columns = set(input_data.columns) & set(headers)
    for col in common_columns:
        transformed_data[col] = input_data[col]

    # Save the transformed data
    transformed_data.to_excel(output_path, index=False, engine='openpyxl')
    print(f"Transformed data has been saved to {output_path}")

# Example usage
template_file = "demo.xlsx"  # Path to the Excel template
input_file = "input_data.csv"    # Path to your input data file
output_file = "transformed_data.xlsx"  # Output file path

transform_data_to_template(input_file, template_file, output_file)