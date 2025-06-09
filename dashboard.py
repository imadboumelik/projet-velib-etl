import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium
import os
import sys

# Ajouter le chemin pour accéder aux autres scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Imports
from extract import telecharger_donnees_velib
from transform import transformer_velib

# Étapes ETL : extraction + transformation
telecharger_donnees_velib()
df = transformer_velib()
df["etat"] = df["etat"].fillna("").astype(str)

# Configuration Streamlit
st.set_page_config(page_title="Dashboard Vélib Paris", layout="wide")
st.title("Dashboard interactif Vélib – Données en direct")

# Affichage de la date de mise à jour
if "mise_a_jour" in df.columns and df["mise_a_jour"].notna().any():
    date_maj = pd.to_datetime(df["mise_a_jour"].dropna().iloc[0])
    st.markdown(f"Données mises à jour le : {date_maj.strftime('%d/%m/%Y %H:%M')}")

# Filtres interactifs
st.sidebar.header("Filtres")
nom_choisi = st.sidebar.text_input("Filtrer par nom de station")
etat_choisi = st.sidebar.selectbox("Filtrer par statut", ["Tous", "OPEN", "CLOSED"])

df_filtered = df.copy()
if nom_choisi:
    df_filtered = df_filtered[df_filtered["nom"].str.contains(nom_choisi, case=False, na=False)]
if etat_choisi != "Tous":
    df_filtered = df_filtered[df_filtered["etat"].str.upper() == etat_choisi]

# Carte Folium interactive
st.subheader("Carte des stations Vélib")
carte = folium.Map(location=[48.8566, 2.3522], zoom_start=13)

for _, row in df_filtered.iterrows():
    couleur = "green" if row["etat"].upper() == "OPEN" else "red"
    lat, lon = row["latitude"], row["longitude"]
    url_streetview = f"https://www.google.com/maps?q=&layer=c&cbll={lat},{lon}"
    popup_html = f"""
        <b>{row['nom']}</b><br>
        Vélos disponibles : {row['nb_velos_dispo']}<br>
        Electriques : {row['electriques']} | Mécaniques : {row['mecaniques']}<br>
        <a href='{url_streetview}' target='_blank'>Voir en Street View</a>
    """
    folium.CircleMarker(
        location=[lat, lon],
        radius=5,
        popup=folium.Popup(popup_html, max_width=300),
        color=couleur,
        fill=True,
        fill_opacity=0.7
    ).add_to(carte)

st_folium(carte, height=500, width=1000)

# Analyse statistique
st.subheader("Analyse statistique")

col1, col2 = st.columns(2)

with col1:
    top = df_filtered.sort_values(by="nb_velos_dispo", ascending=False).head(10)
    st.write("Top 10 stations avec le plus de vélos disponibles")
    st.dataframe(top[["nom", "nb_velos_dispo", "mecaniques", "electriques"]])

with col2:
    st.write("Répartition des types de vélos")
    total_meca = df_filtered["mecaniques"].sum()
    total_elec = df_filtered["electriques"].sum()
    fig1 = px.pie(
        names=["Mécaniques", "Électriques"],
        values=[total_meca, total_elec],
        title="Types de vélos"
    )
    st.plotly_chart(fig1, use_container_width=True)

# Statut des stations
nb_open = (df_filtered["etat"].str.upper() == "OPEN").sum()
nb_closed = (df_filtered["etat"].str.upper() == "CLOSED").sum()

fig2 = px.bar(
    x=["OPEN", "CLOSED"],
    y=[nb_open, nb_closed],
    color=["OPEN", "CLOSED"],
    color_discrete_map={"OPEN": "green", "CLOSED": "red"},
    title="Statut des stations",
    labels={"x": "Statut", "y": "Nombre"}
)
st.plotly_chart(fig2, use_container_width=True)

# Export CSV
st.subheader("Téléchargement des données filtrées")
csv_export = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button("Télécharger (CSV)", csv_export, "velib_filtre.csv", "text/csv")
