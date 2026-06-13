import pandas as pd
from faker import Faker
import random

# Initialisiere Faker für deutsche Daten
fake = Faker('de_DE')


def generate_large_address_dataset(num_records=100000):
    data = []
    print(f"Generiere {num_records} Datensätze...")

    for i in range(1, num_records + 1):
        data.append({
            'kunden_id': i,
            'strasse': fake.street_name(),
            'hausnummer': fake.building_number(),
            'plz': fake.postcode(),
            'stadt': fake.city()
        })

    df = pd.DataFrame(data)

    # Als Parquet speichern
    output_file = '../../import_data/adressen.csv'
    df.to_csv(output_file)
    print(f"Fertig! Datei gespeichert unter: {output_file}")
    print(
        f"Dateigröße: {pd.io.common.os.path.getsize(output_file) / 1024 / 1024:.2f} MB")


# Ausführen der Funktion
generate_large_address_dataset(100000)
