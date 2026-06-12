import pandas as pd

# Erstellung der Adressdaten
data = {
    "kunden_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "strasse": ["Hauptstr. 1", "Nebenweg 5", "Waldweg 12", "Marktplatz 3", "Gartenstr. 9", "Hauptstr. 1", "Bahnhofstr. 8", "Leerer Weg 0"],
    "stadt": ["Berlin", "München", "Hamburg", "Köln", "Frankfurt", "Berlin", "Stuttgart", "Bremen"],
    "plz": ["10115", "80331", "20095", "50667", "60311", "10115", "70173", "28195"]
}

df = pd.DataFrame(data)
df.to_parquet('../import_data/adressen.parquet')
