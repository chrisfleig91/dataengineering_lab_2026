import pandas as pd
import time
import json
import datetime
from sqlalchemy import create_engine

DB_URL = "postgresql://admin:secretpassword@localhost:5432/workshop_db"
JSON_FILE = "../../import_data/bestellungen.json"

with open(JSON_FILE, 'r', encoding='UTF-8') as f:
    json_data = json.load(f)

df_bestellpositionen = pd.json_normalize(
    json_data, record_path=['positionen'], meta=['bestell_id'])

df_bestellungen = pd.json_normalize(
    json_data)

df_bestellungen = df_bestellungen.drop(columns=['positionen'])

df_bestellungen['bestelldatum'] = pd.to_datetime(
    df_bestellungen['bestelldatum'], errors='coerce')

df_bestellpositionen['_modtime'] = datetime.datetime.fromtimestamp(
    time.time()).strftime('%Y-%m-%d %H:%M:%S')

df_bestellungen['_modtime'] = datetime.datetime.fromtimestamp(
    time.time()).strftime('%Y-%m-%d %H:%M:%S')

print(df_bestellungen.head())
print(df_bestellpositionen.head())

try:
    # Datenbankverbindung öffnen und Daten laden
    db_connect = create_engine(DB_URL, connect_args={
        "options": "-csearch_path=staging"})

    # Importieren der neuen Kunden
    df_bestellungen.to_sql('bestellung_staging', db_connect,
                           if_exists='replace', index=False)
    df_bestellpositionen.to_sql(
        'bestellpositionen_staging', db_connect, if_exists='replace', index=False)
    print(
        f"Erfolgreich {len(df_bestellungen)} Zeilen in die Tabelle 'bestellung_staging' importiert.")
    print(
        f"Erfolgreich {len(df_bestellpositionen)} Zeilen in die Tabelle 'bestellpositionen_staging' importiert.")


except Exception as e:
    print(f"Fehler beim Import der Daten: {e}")
