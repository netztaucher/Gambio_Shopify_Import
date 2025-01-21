# Importieren der benötigten Python-Bibliotheken
import pandas as pd              # Für Datenverarbeitung und -analyse
import os                       # Für Dateisystem-Operationen
from datetime import datetime   # Für Zeitstempel-Generierung
import html                     # Für HTML-Dekodierung
import re                       # Für reguläre Ausdrücke
import chardet                  # Für Zeichenkodierungserkennung
import argparse                 # Für Kommandozeilen-Argument-Parsing

def detect_encoding(file_path):
    """Erkennt die Zeichenkodierung einer Datei automatisch"""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def detect_delimiter(file_path, encoding):
    """Erkennt das Trennzeichen in CSV-Dateien (Komma oder Semikolon)"""
    with open(file_path, 'r', encoding=encoding) as file:
        first_line = file.readline()
        return ';' if ';' in first_line else ','

def read_csv_file(file_path):
    """Liest eine CSV-Datei mit automatischer Erkennung von Encoding und Delimiter"""
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
    """Entfernt HTML-Tags und dekodiert HTML-Entities"""
    if pd.isna(text):
        return ""
    text = html.unescape(str(text))
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def format_category(category):
    """Formatiert einzelne Kategorien und entfernt überflüssige Leerzeichen"""
    if pd.isna(category):
        return ""
    return ', '.join(cat.strip() for cat in str(category).split('+'))

def join_categories(x):
    """Verbindet mehrere Kategorien zu einem String"""
    valid_categories = [format_category(cat) for cat in x if pd.notna(cat)]
    return ', '.join(valid_categories) if valid_categories else ''

def create_seo_handle(title, product_id):
    """Erstellt SEO-freundliche URLs aus Produkttiteln und IDs"""
    # Umlaute ersetzen und Kleinbuchstaben verwenden
    clean_title = title.lower()
    clean_title = clean_title.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    # Nicht-alphanumerische Zeichen durch Bindestriche ersetzen
    clean_title = re.sub(r'[^a-z0-9\-]', '-', clean_title)
    # Mehrfache Bindestriche durch einzelne ersetzen
    clean_title = re.sub(r'-+', '-', clean_title)
    clean_title = clean_title.strip('-')
    return f"{clean_title}-{product_id}"

def main():
    """Hauptfunktion zur Verarbeitung der Gambio-CSV-Dateien und Erstellung der Shopify-Import-Datei"""
    # Kommandozeilen-Argumente definieren
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, help='Anzahl der zu exportierenden Zeilen')
    parser.add_argument('--image-prefix', type=str, default='https://netztaucher.com/original_images/', 
                      help='Präfix für Bild-URLs')
    args = parser.parse_args()

    # Verzeichnispfade bestimmen
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir = os.path.join(script_dir, "csv_files")

    # Eingabedateien definieren
    products_file = os.path.join(csv_dir, "products.csv")
    products_desc_file = os.path.join(csv_dir, "products_description.csv")
    categories_desc_file = os.path.join(csv_dir, "categories_description.csv")
    products_categories_file = os.path.join(csv_dir, "products_to_categories.csv")

    # CSV-Dateien einlesen
    products_df = read_csv_file(products_file)
    products_desc_df = read_csv_file(products_desc_file)
    categories_desc_df = read_csv_file(categories_desc_file)
    products_categories_df = read_csv_file(products_categories_file)

    # Prüfen ob alle Dateien erfolgreich gelesen wurden
    if any(df is None for df in [products_df, products_desc_df, categories_desc_df, products_categories_df]):
        print("Fehler: Mindestens eine erforderliche Datei konnte nicht gelesen werden.")
        return

    # Filtern nach deutscher Sprache (language_id = 2)
    products_desc_df = products_desc_df[products_desc_df['language_id'] == 2]
    categories_desc_df = categories_desc_df[categories_desc_df['language_id'] == 2]

    # Daten zusammenführen
    merged_df = products_df.merge(products_desc_df, on='products_id')
    categories = products_categories_df.merge(categories_desc_df, on='categories_id')
    category_groups = categories.groupby('products_id')['categories_name'].apply(join_categories).reset_index()
    final_df = merged_df.merge(category_groups, on='products_id', how='left')

    # Shopify-Dataframe erstellen und befüllen
    shopify_df = pd.DataFrame()
    # Alle erforderlichen Shopify-Spalten mit entsprechenden Werten befüllen
    shopify_df['Handle'] = final_df.apply(lambda x: create_seo_handle(x['products_name'], x['products_id']), axis=1)
    shopify_df['Command'] = 'MERGE'
    shopify_df['Title'] = final_df['products_name'].fillna('')
    shopify_df['Body HTML'] = final_df['products_description'].apply(clean_html)
    # ... [weitere Spalten]

    # Optional: Anzahl der Zeilen begrenzen
    if args.limit:
        shopify_df = shopify_df.head(args.limit)

    # Ausgabeverzeichnis erstellen
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # Zeitstempel für Dateinamen generieren
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Ausgabedateien erstellen (CSV und Excel)
    csv_output_file = os.path.join(output_dir, f'shopify_import_{timestamp}.csv')
    excel_output_file = os.path.join(output_dir, f'shopify_import_{timestamp}.xlsx')
    
    # Dateien speichern
    shopify_df.to_csv(csv_output_file, index=False, sep=';', encoding='utf-8')
    shopify_df.to
