# Gambio zu Shopify CSV-Konverter

Dieses Python-Skript konvertiert Produktdaten aus dem Gambio-Shop-System in ein Shopify-kompatibles CSV-Format. Es werden die folgenden Tabellen sls CSV export und nach csv_files kopiert:
- categories_description
- products_description
- products_to_categories
- products

## Funktionen

- Automatische Erkennung von Dateikodierung und Trennzeichen
- Bereinigung von HTML-Tags
- SEO-freundliche Handle-Generierung
- Kategorie-Formatierung
- Export als CSV und Excel
- Unterstützung für Bildpräfixe
- Optionale Begrenzung der Exportzeilen

## Installation

1. Repository klonen:
```bash
git clone [repository-url]
cd gambio-to-shopify-converter
```

2. Virtuelle Umgebung erstellen und aktivieren:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

## Verwendung

1. Erstellen Sie einen Ordner `csv_files` im Projektverzeichnis
2. Legen Sie folgende Gambio-CSV-Dateien in den `csv_files` Ordner:
   - products.csv
   - products_description.csv
   - categories_description.csv
   - products_to_categories.csv

3. Skript ausführen:
```bash
python converter.py
```

### Optionale Parameter

- `--limit`: Begrenzt die Anzahl der zu exportierenden Zeilen
- `--image-prefix`: Setzt einen benutzerdefinierten Präfix für Bild-URLs

Beispiel:
```bash
python converter.py --limit 100 --image-prefix "https://meinshop.de/images/"
```

## Ausgabe

Das Skript erstellt zwei Dateien im `output` Verzeichnis:
- Eine CSV-Datei (UTF-8, Semikolon-getrennt)
- Eine Excel-Datei

Die Ausgabedateien enthalten einen Zeitstempel im Format: `shopify_import_YYYYMMDD_HHMMSS`

## Systemanforderungen

- Python 3.8 oder höher
- Erforderliche Python-Pakete:
  - pandas >= 2.0.0
  - chardet >= 5.0.0
  - openpyxl >= 3.1.2

## Lizenz

Dieses Projekt ist unter der GNU General Public License v3.0 lizenziert.

Copyright (C) 2025

Dieses Programm ist freie Software. Sie können es unter den Bedingungen der GNU General Public License, wie von der Free Software Foundation veröffentlicht, weitergeben und/oder modifizieren, entweder gemäß Version 3 der Lizenz oder (nach Ihrer Option) jeder späteren Version.

Die Veröffentlichung dieses Programms erfolgt in der Hoffnung, dass es Ihnen von Nutzen sein wird, aber OHNE IRGENDEINE GARANTIE, sogar ohne die implizite Garantie der MARKTREIFE oder der VERWENDBARKEIT FÜR EINEN BESTIMMTEN ZWECK. Details finden Sie in der GNU General Public License.

Sie sollten ein Exemplar der GNU General Public License zusammen mit diesem Programm erhalten haben. Falls nicht, siehe <https://www.gnu.org/licenses/>.

## Kontakt

netztaucher | digitalagentur
https://netztaucher.com/kontakt
