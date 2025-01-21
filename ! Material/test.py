import pandas as pd
import os
import logging
from html import unescape
from datetime import datetime
import csv
import chardet

logging.basicConfig(
    filename=f'csv_conversion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def detect_delimiter(file_path, encoding):
    with open(file_path, 'r', encoding=encoding) as file:
        first_line = file.readline()
        return ';' if first_line.count(';') > first_line.count(',') else ','

def load_csv_file(filename):
    file_path = os.path.join('csv_files', filename)
    try:
        encoding = detect_encoding(file_path)
        delimiter = detect_delimiter(file_path, encoding)
        
        logging.info(f"Datei {filename}: Erkannte Kodierung: {encoding}, Trennzeichen: {delimiter}")
        
        df = pd.read_csv(
            file_path,
            encoding=encoding,
            sep=delimiter,
            quotechar='"',
            quoting=csv.QUOTE_ALL,
            on_bad_lines='skip',
            na_values=[''], keep_default_na=True
        )
        df = df.fillna('')
        return df
    except Exception as e:
        logging.error(f"Fehler beim Laden von {filename}: {str(e)}")
        raise

def clean_html_entities(text):
    return unescape(text) if isinstance(text, str) else text

try:
    categories_desc_df = load_csv_file('categories_description.csv')
    products_desc_df = load_csv_file('products_description.csv')
    products_df = load_csv_file('products.csv')
    products_to_categories_df = load_csv_file('products_to_categories.csv')
    try:
        manufacturers_df = load_csv_file('manufacturers.csv')
    except FileNotFoundError:
        manufacturers_df = None
        print("Hinweis: manufacturers.csv nicht gefunden. Vendor-Feld wird leer gelassen.")

    categories_df = categories_desc_df[categories_desc_df['language_id'] == 2].copy()
    products_desc_df = products_desc_df[products_desc_df['language_id'] == 2].copy()

    categories_df['categories_description'] = categories_df['categories_description'].apply(clean_html_entities)
    products_desc_df['products_description'] = products_desc_df['products_description'].apply(clean_html_entities)

    merged_data = pd.merge(products_df, products_desc_df, on='products_id', how='left')
    merged_data = pd.merge(merged_data, products_to_categories_df, on='products_id', how='left')
    merged_data = pd.merge(merged_data, categories_df, on='categories_id', how='left')
    
    def get_manufacturer_name(manufacturers_df, manufacturer_id):
        if manufacturers_df is None:
            return ''
        matched_manufacturer = manufacturers_df[manufacturers_df['manufacturers_id'] == manufacturer_id]
        if not matched_manufacturer.empty:
            return matched_manufacturer.iloc[0]['manufacturers_name']
        return ''
    
    merged_data['manufacturers_name'] = merged_data['manufacturers_id'].apply(lambda x: get_manufacturer_name(manufacturers_df, x))

    matrixify_df = pd.DataFrame()
    matrixify_df['Handle'] = merged_data['products_model']
    matrixify_df['Command'] = 'MERGE'
    matrixify_df['Title'] = merged_data['products_name']
    matrixify_df['Body HTML'] = merged_data['products_description']
    matrixify_df['Vendor'] = merged_data['manufacturers_name']
    matrixify_df['Type'] = ''
    matrixify_df['Tags'] = ''
    matrixify_df['Status'] = 'active'
    matrixify_df['Published'] = 'true'
    matrixify_df['Category'] = merged_data['categories_name']
    matrixify_df['Variant ID'] = merged_data['products_id']
    matrixify_df['Variant SKU'] = merged_data['products_model']
    matrixify_df['Variant Price'] = merged_data['products_price']
    matrixify_df['Variant Inventory Qty'] = merged_data['products_quantity']
    matrixify_df['Image Src'] = merged_data['products_image']

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_file = f'shopify_import_{timestamp}.csv'
    
    matrixify_df.to_csv(
        output_file,
        index=False,
        encoding='utf-8',
        sep=';',
        quoting=csv.QUOTE_ALL
    )
    
    logging.info(f"Export erfolgreich in {output_file} gespeichert")

except Exception as e:
    logging.error(f"Ein Fehler ist aufgetreten: {str(e)}")
    raise

logging.info("Skript erfolgreich beendet")
