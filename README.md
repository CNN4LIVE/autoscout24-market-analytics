# AutoScout24 Market Analytics & Price Prediction 🚗📊

Ein End-to-End Data Science Projekt zur Analyse von Gebrauchtwagen-Marktdaten von AutoScout24 sowie zur Entwicklung von Machine-Learning-Modellen zur Verkaufspreisvorhersage.

---

## 📌 Projektübersicht

Dieses Projekt deckt den vollständigen Lebenszyklus eines Data-Science-Projekts ab[cite: 2, 3]:
1. **Datenbereinigung & Preprocessing:** Bereinigung des Rohdatensatzes von Duplikaten, Ausreißern und fehlerhaften Daten.
2. **Explorative Datenanalyse (EDA):** Identifikation von Markttrends, Herstellerverteilungen und Feature-Korrelationen.
3. **Machine Learning Pipeline:** Vergleich von Regressionsmodellen zur präzisen Vorhersage von Fahrzeugpreisen.
4. **Interaktives Dashboard:** Visualisierung der Analyseergebnisse und ML-Prognosen über eine Streamlit-Web-App[cite: 1, 3].

---

## 📂 Projektstruktur

```text
autoscout24-market-analytics/
├── data/
│   ├── autoscout24.csv          # Rohdaten
│   └── autoscout24_cleaned.csv  # Bereinigter Datensatz
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb   # EDA & Marktanalysen
│   └── 02_machine_learning_modeling.ipynb   # ML-Training & Evaluierung
├── src/
│   ├── __init__.py
│   ├── data_loader.py           # Skript zur automatisierten Datenbereinigung
│   └── model_pipeline.py        # ML-Training & Pipeline-Module
├── app.py                       # Streamlit Dashboard App
├── requirements.txt             # Abhängigkeiten
├── .gitignore
└── README.md
