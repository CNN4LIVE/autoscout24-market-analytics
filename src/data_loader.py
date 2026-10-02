import pandas as pd
import numpy as np

def load_and_clean_data(raw_csv_path="data/autoscout24.csv", output_cleaned_path="data/autoscout24_cleaned.csv"):
    """
    Lädt die Rohdaten aus AutoScout24, führt eine Datenbereinigung durch
    und speichert den bereinigten Datensatz als neue CSV-Datei ab.
    """
    print(f"Lade Rohdaten aus: {raw_csv_path}...")
    df = pd.read_csv(raw_csv_path)
    print(f"Ursprüngliche Form (Zeilen, Spalten): {df.shape}")

    # 1. Duplikate entfernen
    initial_rows = len(df)
    df = df.drop_duplicates()
    print(f"Entfernte Duplikate: {initial_rows - len(df)}")

    # 2. Leere oder unvollständige Zeilen prüfen/behandeln
    # Wichtige Schlüsselspalten dürfen keine Fehlwerte enthalten
    key_columns = ['make', 'model', 'price', 'mileage', 'hp', 'year']
    existing_key_cols = [col for col in key_columns if col in df.columns]
    df = df.dropna(subset=existing_key_cols)

    # 3. Datentypen korrigieren
    numeric_cols = ['price', 'mileage', 'hp', 'year']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Erneutes Entfernen von Zeilen, bei denen die Konvertierung fehlschlug (NaN)
    df = df.dropna(subset=[col for col in numeric_cols if col in df.columns])

    # 4. Plausibilitäts-Checks / Ungültige Werte herausfiltern
    # Preis > 0, Kilometerstand >= 0, PS > 0, Baujahr realistisch (z.B. 1900 bis 2026)
    if 'price' in df.columns:
        df = df[df['price'] > 0]
    if 'mileage' in df.columns:
        df = df[df['mileage'] >= 0]
    if 'hp' in df.columns:
        df = df[df['hp'] > 0]
    if 'year' in df.columns:
        df = df[(df['year'] >= 1900) & (df['year'] <= 2026)]

    # 5. Bereinigte CSV abspeichern
    df.to_csv(output_cleaned_path, index=False)
    print(f"Bereinigung abgeschlossen! Bereinigter Datensatz gespeichert unter: {output_cleaned_path}")
    print(f"Endgültige Form (Zeilen, Spalten): {df.shape}")

    return df

if __name__ == "__main__":
    load_and_clean_data()
    
    





    