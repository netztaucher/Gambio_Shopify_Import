import pandas as pd

def validate_columns(dataframe, required_columns, filename):
    """Validate required columns in a dataframe."""
    missing_columns = [col for col in required_columns if col not in dataframe.columns]
    if missing_columns:
        raise ValueError(f"Fehlende Spalten in {filename}: {missing_columns}")

def transform_to_matrixify(products, descriptions, product_categories):
    """Transform data to Matrixify format."""
    # Validating required columns
    validate_columns(products, ['products_id'], "products.csv")
    validate_columns(descriptions, ['products_id', 'language_id', 'products_name'], "products_description.csv")
    validate_columns(product_categories, ['products_id', 'categories_id'], "products_to_categories.csv")
    
    # Merge data
    combined = pd.merge(products, descriptions, on="products_id", how="left")
    combined = pd.merge(combined, product_categories, on="products_id", how="left")
    
    # Add Matrixify-specific columns (adjust as needed)
    combined['Matrixify_Category'] = combined['categories_id']
    
    return combined

def process_files(input_files, output_file):
    """Process input files and transform into Matrixify-compatible output."""
    data_frames = {}
    
    # Read and validate each file
    for file_name, (file_path, expected_columns) in input_files.items():
        print(f"Verarbeite {file_name} | Erwartete Spaltenanzahl: {len(expected_columns)}")
        df = pd.read_csv(file_path, delimiter=";", dtype=str)
        validate_columns(df, expected_columns, file_name)
        data_frames[file_name] = df

    # Transform data
    transformed_data = transform_to_matrixify(
        products=data_frames['products'],
        descriptions=data_frames['products_description'],
        product_categories=data_frames['products_to_categories']
    )
    
    # Save to output
    transformed_data.to_csv(output_file, index=False)
    print(f"Daten wurden erfolgreich in '{output_file}' gespeichert.")

# Define input files and their expected structures
input_files = {
    "products": ("products.csv", ["products_id", "products_image", "products_price"]),
    "products_description": ("products_description.csv", ["products_id", "language_id", "products_name"]),
    "products_to_categories": ("products_to_categories.csv", ["products_id", "categories_id"]),
}

# Output file
output_file = "matrixify_export.csv"

# Process the files
try:
    process_files(input_files, output_file)
except Exception as e:
    print(f"Fehler: {e}")