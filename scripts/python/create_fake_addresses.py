import pandas as pd
from faker import Faker
from sqlalchemy import create_engine
import random

# Initialisiere Faker für deutsche Daten
fake = Faker('de_DE')

# Konfigurationsvariablen
# Connection Schema: "db_engine://user:passwort@host:port/database_name"
DB_URL = "postgresql://admin:secretpassword@localhost:5432/workshop_db"


def generate_large_address_dataset(num_records=100000):
    db_connect = create_engine(DB_URL, connect_args={
                               "options": "-csearch_path=public"})
    df_sql = pd.read_sql(
        "SELECT * FROM kunde", db_connect)

    df_sql['registrierungsdatum'] = pd.to_datetime(
        df_sql['registrierungsdatum'], errors='coerce')

    # Abgleich der CSV Daten mit SQL Daten
    existing_ids = df_sql['kunden_id'].tolist()

    data = []
    print(f"Generiere {num_records} Datensätze...")

    for i in range(1, num_records + 1):
        data.append({
            'kunden_id': random.choice(existing_ids),
            'strasse': fake.street_name(),
            'hausnummer': fake.building_number(),
            'plz': fake.postcode(),
            'stadt': fake.city()
        })

    df = pd.DataFrame(data)

    # Als Parquet speichern
    output_file = '../../import_data/adressen.parquet'
    df.to_parquet(output_file, index=False, compression='snappy')
    print(f"Fertig! Datei gespeichert unter: {output_file}")
    print(
        f"Dateigröße: {pd.io.common.os.path.getsize(output_file) / 1024 / 1024:.2f} MB")


# Ausführen der Funktion
generate_large_address_dataset(100000)
