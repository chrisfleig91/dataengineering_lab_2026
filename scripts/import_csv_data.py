import pandas as pd
import numpy as np
import hashlib
from sqlalchemy import create_engine
import datetime
import time
# Funktion um den Zeilen Hash zu erstellen


def generate_row_hash(row):
    def normalize_val(val):
        # Check auf NaT (Pandas Datetime)
        if pd.isna(val):
            return "NULL"
        # Check auf None/NaN (Python/Numpy)
        if val is None or (isinstance(val, float) and np.isnan(val)):
            return "NULL"
        # Sonst den Wert als String behandeln
        return str(val).strip()

    row_string = "".join([normalize_val(val) for val in row.values])
    return hashlib.md5(row_string.encode()).hexdigest()


# Konfigurationsvariablen
# Connection Schema: "db_engine://user:passwort@host:port/database_name"
DB_URL = "postgresql://admin:secretpassword@localhost:5432/workshop_db"
CSV_FILE = "../import_data/kunden.csv"

# Lade CSV Datei
df_csv = pd.read_csv(CSV_FILE)
# Bereinigen und Transformieren der Daten
df_csv = df_csv.drop_duplicates(subset=['kunden_id'])

df_csv['registrierungs_datum'] = pd.to_datetime(
    df_csv['registrierungs_datum'], errors='coerce')

if 'registrierungs_datum' in df_csv.columns:
    df_csv = df_csv.rename(
        columns={'registrierungs_datum': 'registrierungsdatum'})

df_csv['neukunde'] = df_csv['status'] == 'neu'

df_csv['status'] = np.where(
    df_csv['status'].isin(['aktiv', 'neu']), True, False)
if 'status' in df_csv.columns:
    df_csv = df_csv.rename(
        columns={'status': 'kunden_status'})

df_csv['_modtime'] = datetime.datetime.fromtimestamp(
    time.time()).strftime('%Y-%m-%d %H:%M:%S')

try:
    # Datenbankverbindung öffnen und Daten laden
    db_connect = create_engine(DB_URL, connect_args={
                               "options": "-csearch_path=staging"})

    # Importieren der neuen Kunden
    df_csv.to_sql('kunde_staging', db_connect,
                  if_exists='replace', index=False)
    print(
        f"Erfolgreich {len(df_csv)} Zeilen in die Tabelle 'kunde' importiert.")

except Exception as e:
    print(f"Fehler beim Import der Daten: {e}")
