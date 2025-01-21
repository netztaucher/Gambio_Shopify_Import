# benötigte Modiule laden
import pandas as pd
import os
from datetime import datetime
import html
import re
import chardet
import argparse

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def detect_delimiter(file_path, encoding):
    with open(file_path, 'r', encoding=encoding) as file:
        first_line = file.readline()
        if ';' in first_line:
            return ';'
        return ','

def read_csv_file(file_path):
    if not os.path.exists(file_path):
        print(f"Fehler: Die Datei {file_path} wurde nicht gefunden.")
        return None
        
    encoding = detect_encoding(file_path)
    delimiter = detect_delimiter(file_path, encoding)
    try:
        df = pd.read_csv(file_path, encoding=encoding, sep=delimiter, low_memory=False)
        return df
    except Exception as e:
        print(f"Fehler beim Lesen der Datei {file_path}: {str(e)}")
        return None

def clean_html(text):
    if pd.isna(text):
        return ""
    text = html.unescape(str(text))
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def format_category(category):
    if pd.isna(category):
        return ""
    return ', '.join(cat.strip() for cat in str(category).split('+'))

def join_categories(x):
    valid_categories = [format_category(cat) for cat in x if pd.notna(cat)]
    return ', '.join(valid_categories) if valid_categories else ''

def create_seo_handle(title, product_id):
    clean_title = title.lower()
    clean_title = clean_title.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    clean_title = re.sub(r'[^a-z0-9\-]', '-', clean_title)
    clean_title = re.sub(r'-+', '-', clean_title)
    clean_title = clean_title.strip('-')
    return f"{clean_title}-{product_id}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, help='Anzahl der zu exportierenden Zeilen')
    parser.add_argument('--image-prefix', type=str, default='https://netztaucher.com/original_images/', 
                      help='Präfix für Bild-URLs')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir = os.path.join(script_dir, "csv_files")

    products_file = os.path.join(csv_dir, "products.csv")
    products_desc_file = os.path.join(csv_dir, "products_description.csv")
    categories_desc_file = os.path.join(csv_dir, "categories_description.csv")
    products_categories_file = os.path.join(csv_dir, "products_to_categories.csv")

    products_df = read_csv_file(products_file)
    products_desc_df = read_csv_file(products_desc_file)
    categories_desc_df = read_csv_file(categories_desc_file)
    products_categories_df = read_csv_file(products_categories_file)

    if any(df is None for df in [products_df, products_desc_df, categories_desc_df, products_categories_df]):
        print("Fehler: Mindestens eine erforderliche Datei konnte nicht gelesen werden.")
        return

    products_desc_df = products_desc_df[products_desc_df['language_id'] == 2]
    categories_desc_df = categories_desc_df[categories_desc_df['language_id'] == 2]

    merged_df = products_df.merge(products_desc_df, on='products_id')
    categories = products_categories_df.merge(categories_desc_df, on='categories_id')
    category_groups = categories.groupby('products_id')['categories_name'].apply(join_categories).reset_index()
    final_df = merged_df.merge(category_groups, on='products_id', how='left')

    shopify_df = pd.DataFrame()
    shopify_df['Handle'] = final_df.apply(lambda x: create_seo_handle(x['products_name'], x['products_id']), axis=1)
    shopify_df['Command'] = 'MERGE'
    shopify_df['Title'] = final_df['products_name'].fillna('')
    shopify_df['Body HTML'] = final_df['products_description'].apply(clean_html)
    shopify_df['Vendor'] = ''
    shopify_df['Type'] = ''
    shopify_df['Tags'] = final_df['categories_name'].fillna('')
    shopify_df['Tags Command'] = 'MERGE'
    shopify_df['Status'] = final_df['products_status'].map({1: 'active', 0: 'draft'})
    shopify_df['Image Src'] = args.image_prefix + final_df['products_image'].fillna('')
    shopify_df['Image Command'] = 'MERGE'
    shopify_df['Image Position'] = ''
    shopify_df['Image Alt Text'] = final_df['products_name'].fillna('')
    shopify_df['Variant Price'] = final_df['products_price'].fillna(0)
    shopify_df['Status'] = 'Active'
    shopify_df['Variant Inventory Qty'] = final_df['products_quantity'].fillna(0)
    shopify_df['Variant Inventory Tracker'] = 'shopify'
    shopify_df['Variant SKU'] = final_df['products_model']
    shopify_df['Category: ID'] = 'ae-3-1-6'
    shopify_df['Custom Collections'] = final_df['categories_name'].fillna('')

    if args.limit:
        shopify_df = shopify_df.head(args.limit)

    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_output_file = os.path.join(output_dir, f'shopify_import_{timestamp}.csv')
    excel_output_file = os.path.join(output_dir, f'shopify_import_{timestamp}.xlsx')
    
    shopify_df.to_csv(csv_output_file, index=False, sep=';', encoding='utf-8')
    shopify_df.to_excel(excel_output_file, index=False, engine='openpyxl')
    
    print(f"CSV-Datei erfolgreich erstellt: {csv_output_file}")
    print(f"Excel-Datei erfolgreich erstellt: {excel_output_file}")

if __name__ == "__main__":
    main()
