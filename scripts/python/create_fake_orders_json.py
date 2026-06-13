import pandas as pd
from faker import Faker
from sqlalchemy import create_engine
import random
import json

fake = Faker('de_DE')

# Konfigurationsvariablen
# Connection Schema: "db_engine://user:passwort@host:port/database_name"
JSON_FILE = "../../import_data/bestellungen.json"
DB_URL = "postgresql://admin:secretpassword@localhost:5432/workshop_db"


def generate_complex_orders(num_orders=100):
    db_connect = create_engine(DB_URL, connect_args={
                               "options": "-csearch_path=public"})
    df_sql = pd.read_sql(
        "SELECT * FROM kundenadresse", db_connect)

    # Abgleich der CSV Daten mit SQL Daten
    existing_ids = df_sql['kundenadress_id'].tolist()

    orders = []
    product_catalog = {
        'Laptop': 999.00, 'Monitor': 200.00, 'Tastatur': 50.00,
        'Maus': 25.00, 'Webcam': 80.00, 'Headset': 120.00
    }

    for i in range(num_orders):
        # Zufällige Anzahl an Produkten pro Bestellung (1 bis 4)
        num_items = random.randint(1, 4)
        selected_products = random.sample(
            list(product_catalog.items()), num_items)

        positionen = [
            {"produkt": item[0], "preis": item[1]}
            for item in selected_products
        ]

        orders.append({
            'bestell_id': 1000 + i,
            'kundenadress_id': random.choice(existing_ids),
            'bestelldatum': fake.date_between(start_date='-1y', end_date='today').isoformat(),
            'positionen': positionen
        })

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, indent=4)

    print(f"{num_orders} komplexe Bestellungen wurden in 'data/bestellungen.json' gespeichert.")


generate_complex_orders()
