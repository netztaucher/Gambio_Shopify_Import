import pandas as pd
import os
from datetime import datetime
import html
import re
import chardet
import argparse


# Funktion zur Erkennung der Kodierung einer Datei
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

# Funktion zur Erkennung des Trennzeichens in einer CSV-Datei
def detect_delimiter(file_path, encoding):
    with open(file_path, 'r', encoding=encoding) as file:
        first_line = file.readline()
        if ';' in first_line:
            return ';'
        return ','

# Funktion zum Einlesen einer CSV-Datei in ein DataFrame
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

# Funktion zur Bereinigung von HTML-Tags aus einem Text
def clean_html(text):
    if pd.isna(text):
        return ""
    text = html.unescape(str(text))
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

# Funktion zur Formatierung von Kategorien
def format_category(category):
    if pd.isna(category):
        return ""
    return ', '.join(cat.strip() for cat in str(category).split('+'))