import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from pathlib import Path

# Pfade vorbereiten
script_dir = Path(__file__).parent
csv_path = script_dir / "query.csv"
volc_path = script_dir / "volc_longlat.csv"

# Daten laden
df = pd.read_csv(csv_path)
try:
    volc = pd.read_csv(volc_path)
except FileNotFoundError:
    volc = None

# ================================
# Streamlit Setup
# ================================
st.set_page_config(page_title="Erdbeben Dashboard", layout="wide")
st.title("🌍 Erdbeben Dashboard")

# Navigation: Seiten-Auswahl
page = st.sidebar.radio(
    "Navigation",
    ["ℹ️ Einführung", "1️⃣ Epizentren", "2️⃣ Nach Tiefe", "3️⃣ Nach Stärke + Vulkane"]
)

# ================================
# Seite 1: Einführung
# ================================
if page.startswith("ℹ️"):
    st.header("Einführung")
    st.markdown("""
    Dieses Dashboard zeigt **Erdbeben mit Stärke ≥ 4.5 im Jahr 2020** weltweit.  
    Die Daten stammen vom **[USGS Earthquake Hazards Program](https://earthquake.usgs.gov/earthquakes/search/)**.  
    Zusätzlich werden in einer Grafik auch Vulkane angezeigt.  
    
    **Hinweis:**  
    - Datenquelle: USGS (WGS84, CSV Export)  
    - Epizentren: Längen- und Breitengrad  
    - Stärke: Größe des Bebens  
    - Tiefe: Tiefe des Hypozentrums
    """)

# ================================
# Seite 2: Nur Epizentren
# ================================
elif page.startswith("1"):
    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_global()
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor="lightgray")

    ax.scatter(
        df["longitude"], df["latitude"],
        s=df["mag"],  # Größe abhängig von Stärke
        color="green", alpha=0.6,
        transform=ccrs.PlateCarree()
    )

    st.subheader("Epizentren")
    st.write("")
    st.pyplot(fig)

# ================================
# Seite 3: Nach Tiefe
# ================================
elif page.startswith("2"):
    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_global()
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor="lightgray")

    sc = ax.scatter(
        df["longitude"], df["latitude"],
        c=df["depth"], cmap="coolwarm",
        s=np.exp(df["mag"])/2, alpha=0.7,
        transform=ccrs.PlateCarree()
    )

    st.subheader("Epizentren – eingefärbt nach Tiefe, Punktgröße nach Stärke")
    st.markdown("""
    Die Farben zeigen die Tiefe. 
    - Rot = flache Beben  
    - Blau = tiefe Beben  
    Die Größe der Punkte entspricht der Stärke des Bebens.
    """)
    st.pyplot(fig)

# ================================
# Seite 4: Nach Stärke + Vulkane
# ================================
elif page.startswith("3"):
    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_global()
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor="lightgray")

    sc = ax.scatter(
        df["longitude"], df["latitude"],
        c=df["depth"], cmap="coolwarm",
        s=np.exp(df["mag"])/2, alpha=0.6,
        transform=ccrs.PlateCarree()
    )
    # plt.colorbar(sc, ax=ax, orientation="horizontal", label="Tiefe (km)")

    if volc is not None:
        ax.scatter(
            volc["LONGITUDE"], volc["LATITUDE"],
            marker="^", s=30, color="black",
            transform=ccrs.PlateCarree(), label="Vulkane"
        )
        ax.legend()

    st.subheader("Epizentren – Stärke + Vulkane")
    st.markdown("""
    Die Größe entspricht der Stärke, die Farben der Tiefe. 
    Schwarze Dreiecke = Vulkane.
    """)
    st.pyplot(fig)
