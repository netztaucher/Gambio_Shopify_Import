#!/bin/bash

file_path="/Volumes/daten/Dropbox/!dev/Gambio_Shopify_Import/Kram/komplett.txt"

# Entferne Duplikate und speichere die eindeutigen Begriffe in einer temporären Datei
sort "$file_path" | uniq > "${file_path}.tmp"

# Ersetze die ursprüngliche Datei durch die temporäre Datei
mv "${file_path}.tmp" "$file_path"