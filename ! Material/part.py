import pandas as pd
import os
import logging
from html import unescape
from datetime import datetime
import csv

# Logging-Konfiguration
logging.basicConfig(
    filename=f'csv_conversion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_csv_file(filename):
    return pd.read_csv(
        os.path.join('csv_files', filename),
        encoding='utf-8',
        sep=';',
        quotechar='"',
        quoting=csv.QUOTE_ALL
    )

def clean_html_entities(text):
    if isinstance(text, str):
        return unescape(text)
    return text

try:
    # CSV-Dateien einlesen
    logging.info("Starte das Einlesen der CSV-Dateien")
    
    categories_desc_df = load_csv_file('categories_description_sample.csv')
    products_desc_df = load_csv_file('products_description_sample.csv')
    products_df = load_csv_file('products_sample_sample.csv')
    products_to_categories_df = load_csv_file('products_to_categories_sample.csv')

    # Kategorien verarbeiten
    categories_df = categories_desc_df.copy()
    categories_df['categories_description'] = "hier die beschreibung der kategorie"
    
    # HTML-Entities in Produktbeschreibungen bereinigen
    products_desc_df['products_description'] = products_desc_df['products_description'].apply(clean_html_entities)

    # Zusammenführen der Produkt-Informationen
    merged_products = pd.merge(
        products_df,
        products_desc_df,
        on='products_id',
        how='left'
    )

    # Produkt-Kategorie-Zuordnungen hinzufügen
    final_df = pd.merge(
        merged_products,
        products_to_categories_df,
        on='products_id',
        how='left'
    )

    # Matrixify-Export erstellen
    final_df.to_csv('matrixify_import.csv', index=False, encoding='utf-8')
    logging.info("Export erfolgreich abgeschlossen")

except Exception as e:
    logging.error(f"Ein Fehler ist aufgetreten: {str(e)}")
    raise

logging.info("Skript erfolgreich beendet")
