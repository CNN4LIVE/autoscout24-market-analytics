import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Page Config
st.set_page_config(page_title="AutoScout24 Analytics", page_icon="🚗", layout="wide")

# Daten laden
@st.cache_data
def load_data():
    return pd.read_csv("data/autoscout24_cleaned.csv")

df = load_data()

# Modell trainieren (Cache für Performance)
@st.cache_resource
def train_model(data):
    top_5_makes = data['make'].value_counts().head(5).index.tolist()
    df_top5 = data[data['make'].isin(top_5_makes)].copy()
    
    features = ['make', 'model', 'fuel', 'gear', 'mileage', 'hp', 'year']
    X = df_top5[features]
    y = df_top5['price']
    
    categorical_cols = ['make', 'model', 'fuel', 'gear']
    numeric_cols = ['mileage', 'hp', 'year']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
        ]
    )
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
    ])
    model.fit(X, y)
    return model, top_5_makes

model, top_5_makes = train_model(df)

# Header
st.title("🚗 AutoScout24 Market Analytics & Price Prediction")
st.markdown("Interaktives Dashboard zur Analyse von Gebrauchtwagen-Marktdaten und Preisschätzung.")

# Tabs zur Strukturierung
tab1, tab2, tab3 = st.tabs(["📊 Marktanalyse", "🏆 Top 5 Hersteller", "💡 Preis-Rechner"])

# TAB 1: MARKTRANALYSE
with tab1:
    st.header("Marktüberblick & Kennzahlen")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Anzahl Autos", f"{len(df):,}")
    col2.metric("Durchschnittspreis", f"{df['price'].mean():,.0f} €")
    col3.metric("Durchschn. Laufleistung", f"{df['mileage'].mean():,.0f} km")
    col4.metric("Erfasste Marken", df['make'].nunique())
    
    st.divider()
    
    col_left, col_right = st.columns(2)
    with col_left:
        fig_make = px.histogram(df, x="make", title="Angebote nach Automarke", text_auto=True)
        fig_make.update_xaxes(categoryorder="total descending")
        st.plotly_chart(fig_make, use_container_width=True)
        
    with col_right:
        fig_scatter = px.scatter(
            df.sample(min(3000, len(df))), 
            x="mileage", y="price", color="make", 
            title="Preis vs. Kilometerstand (Stichprobe)",
            labels={"mileage": "Kilometerstand (km)", "price": "Preis (€)"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# TAB 2: TOP 5 HERSTELLER
with tab2:
    st.header("Analyse der Top 5 Hersteller")
    df_top5 = df[df['make'].isin(top_5_makes)]
    
    fig_avg = px.bar(
        df_top5.groupby("make", as_index=False)["price"].mean(),
        x="make", y="price",
        color="make",
        title="Durchschnittlicher Verkaufspreis der Top 5 Hersteller",
        labels={"price": "Durchschnittspreis (€)", "make": "Hersteller"},
        text_auto=".2f"
    )
    st.plotly_chart(fig_avg, use_container_width=True)

# TAB 3: PREIS-RECHNER
with tab3:
    st.header("💡 Gebrauchtwagen-Preisschätzung (Machine Learning)")
    st.write("Gib die Merkmale deines Fahrzeugs ein, um eine Prognose zu erhalten:")
    
    c1, c2, c3 = st.columns(3)
    input_make = c1.selectbox("Hersteller", top_5_makes)
    available_models = df[df['make'] == input_make]['model'].unique().tolist()
    input_model = c2.selectbox("Modell", available_models)
    input_fuel = c3.selectbox("Kraftstoff", df['fuel'].unique().tolist())
    
    c4, c5, c6 = st.columns(3)
    input_gear = c4.selectbox("Getriebe", df['gear'].unique().tolist())
    input_mileage = c5.number_input("Kilometerstand (km)", min_value=0, max_value=500000, value=80000, step=5000)
    input_hp = c6.number_input("Leistung (PS)", min_value=30, max_value=800, value=120, step=10)
    
    input_year = st.slider("Erstzulassungsjahr", min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=2018)
    
    if st.button("Preis schätzen 🚀", type="primary"):
        input_data = pd.DataFrame([{
            'make': input_make,
            'model': input_model,
            'fuel': input_fuel,
            'gear': input_gear,
            'mileage': input_mileage,
            'hp': input_hp,
            'year': input_year
        }])
        
        predicted_price = model.predict(input_data)[0]
        st.success(f"Geschätzter Verkaufspreis: **{predicted_price:,.2f} €**")
