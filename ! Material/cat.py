import pandas as pd
import html
import os
from pathlib import Path

def clean_html_entities(text):
    if isinstance(text, str):
        return html.unescape(text)
    return text

def process_categories():
    # Erstelle den Pfad zum CSV-Verzeichnis
    csv_dir = Path('csv_files')
    
    try:
        # Lese categories_description.csv
        categories_df = pd.read_csv(
            csv_dir / 'categories_description.csv',
            encoding='utf-8',
            sep=';',
            dtype=str
        )
        
        # Bereinige HTML-Entities in allen String-Spalten
        for column in categories_df.select_dtypes(include=['object']):
            categories_df[column] = categories_df[column].apply(clean_html_entities)
        
        # Erstelle Output-Verzeichnis falls nicht vorhanden
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        
        # Exportiere als CSV
        categories_df.to_csv(
            output_dir / 'categories_processed.csv',
            index=False,
            encoding='utf-8',
            sep=';'
        )
        
        # Exportiere als Excel
        categories_df.to_excel(
            output_dir / 'categories_processed.xlsx',
            index=False,
            engine='openpyxl'
        )
        
        print("Verarbeitung erfolgreich abgeschlossen!")
        print(f"Dateien wurden gespeichert in: {output_dir}")
        
    except FileNotFoundError:
        print("Fehler: Die Datei categories_description.csv wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {str(e)}")

if __name__ == "__main__":
    process_categories()
