import pandas as pd
import time
import datetime
from sqlalchemy import create_engine
import duckdb

start_zeit = time.time()

DB_URL = "postgresql://admin:secretpassword@localhost:5432/workshop_db"
PARQUET_FILE = "../../import_data/adressen.parquet"

# df_addresses = pd.read_parquet(PARQUET_FILE)

# stadt_statistik = df_addresses.groupby(
#     'stadt').size().reset_index(name='anzahl_kunden')

# stadt_statistik = stadt_statistik.sort_values(
#     by='anzahl_kunden', ascending=False)

# print(stadt_statistik)
# berlin_kunden = df_addresses[df_addresses['stadt'] == "Berlin"]

# result = pd.read_parquet(PARQUET_FILE)

query = """
    SELECT kunden_id, plz, stadt, strasse, hausnummer
    FROM '../../import_data/adressen.parquet'
"""

df_adressen = duckdb.query(query).df()

df_adressen["adress_id"] = df_adressen.index+1

df_adressen['_modtime'] = datetime.datetime.fromtimestamp(
    time.time()).strftime('%Y-%m-%d %H:%M:%S')

# zeit in parquet mit pandas für groupby stadt und anzahl_kunden 0,2539 Sekunden.
# zeit in parquet mit duckdb für groupby stadt und anzahl_kunden 0,0390 Sekunden.
# print(berlin_kunden.head(100))

try:
    # Datenbankverbindung öffnen und Daten laden
    db_connect = create_engine(DB_URL, connect_args={
                               "options": "-csearch_path=staging"})

    # Importieren der neuen Kunden
    df_adressen.to_sql('adresse_staging', db_connect,
                       if_exists='replace', index=False)
    print(
        f"Erfolgreich {len(df_adressen)} Zeilen in die Tabelle 'adresse_staging' importiert.")
    ende_zeit = time.time()
    dauer = ende_zeit - start_zeit
    print(f"Der Prozess hat {dauer:.4f} Sekunden gedauert.")

except Exception as e:
    print(f"Fehler beim Import der Daten: {e}")
