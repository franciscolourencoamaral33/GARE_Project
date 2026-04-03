import folium
from folium.plugins import MarkerCluster
import pandas as pd
import html
import math
import streamlit as st

# 1. As cores do teu colega
PALETTE = [
    "#1f77b4", "#d62728", "#2ca02c", "#ff7f0e",
    "#9467bd", "#8c564b", "#17becf",
]

# 2. Todos os fatores/detalhes
POPUP_FIELDS = [
    "Dataset", "Resource", "Name", "Country", "Geological Setting",
    "Host Rock / Reservoir", "Deposit Type / Trap Type",
    "Grade / Concentration", "Size / Reserves", "Depth",
    "Temperature", "Status", "Notes"
]

def build_popup(row):
    """Constrói a tabela de detalhes."""
    lines = []
    for field in POPUP_FIELDS:
        value = str(row.get(field, "")).strip()
        if not value or value.lower() in ('nan', 'none', 'null'):
            continue
        lines.append(
            f"<tr><th style='text-align:left; padding:4px 8px 4px 0;'>{html.escape(field)}</th>"
            f"<td style='padding:4px 0;'>{html.escape(value)}</td></tr>"
        )

    if not lines:
        return "<b>Sem detalhes disponíveis</b>"

    return (
        "<div style='min-width:260px; font-family: sans-serif;'>"
        "<table style='border-collapse:collapse'>"
        + "".join(lines)
        + "</table></div>"
    )

def build_folium_map(occurrences):
    # Tratar dados
    if isinstance(occurrences, pd.DataFrame):
        occurrences = occurrences.fillna("")
        data_points = occurrences.to_dict('records')
    else:
        data_points = occurrences

    # Filtrar pontos com coordenadas válidas
    valid_points = []
    for point in data_points:
        lat_raw = str(point.get("Latitude", "")).replace(",", ".")
        lon_raw = str(point.get("Longitude", "")).replace(",", ".")
        
        try:
            if not lat_raw or not lon_raw or lat_raw.lower() in ('nan', 'none') or lon_raw.lower() in ('nan', 'none'):
                continue
            lat = float(lat_raw)
            lon = float(lon_raw)
            if math.isnan(lat) or math.isnan(lon):
                continue
            valid_points.append({"lat": lat, "lon": lon, "data": point})
        except (ValueError, TypeError):
            continue

    if not valid_points:
        return folium.Map(location=[39.5, 15.0], zoom_start=4, tiles="CartoDB positron")

    avg_lat = sum(p["lat"] for p in valid_points) / len(valid_points)
    avg_lon = sum(p["lon"] for p in valid_points) / len(valid_points)

    fmap = folium.Map(location=[avg_lat, avg_lon], zoom_start=4, tiles="CartoDB positron")

    # Lógica ORIGINAL DO TEU COLEGA: Agrupar apenas por Dataset
    def get_category(row):
        dataset = str(row.get("Dataset", "")).strip()
        if dataset and dataset.lower() not in ('nan', 'none'):
            return dataset
        return "Desconhecido"

    categories = sorted({get_category(p["data"]) for p in valid_points})
    color_map = {cat: PALETTE[index % len(PALETTE)] for index, cat in enumerate(categories)}
    clusters = {}

    for cat in categories:
        group = folium.FeatureGroup(name=cat, show=True).add_to(fmap)
        clusters[cat] = MarkerCluster(name=f"{cat}").add_to(group)

    for p in valid_points:
        row = p["data"]
        cat = get_category(row)
        name = str(row.get("Name", "Sem nome")).strip()
        resource = str(row.get("Resource", "Sem recurso")).strip()

        tooltip = name
        if resource and resource != "Sem recurso":
            tooltip += f" | {resource}"

        folium.CircleMarker(
            location=[p["lat"], p["lon"]],
            radius=6,
            color=color_map[cat],
            weight=1,
            fill=True,
            fill_color=color_map[cat],
            fill_opacity=0.85,
            tooltip=tooltip,
            popup=folium.Popup(build_popup(row), max_width=420),
        ).add_to(clusters[cat])

    # === DESENHAR A LEGENDA NATIVAMENTE NO STREAMLIT ===
    if categories:
        st.markdown("**Legenda (Dataset):**")
        cols = st.columns(3) 
        for i, cat in enumerate(categories):
            color = color_map[cat]
            cols[i % 3].markdown(
                f"<div style='display:flex; align-items:center; margin-bottom:4px;'>"
                f"<span style='display:inline-block; width:14px; height:14px; background:{color}; border-radius:50%; margin-right:8px; border:1px solid #aaa;'></span>"
                f"<span style='font-size: 14px;'>{html.escape(cat)}</span>"
                "</div>",
                unsafe_allow_html=True
            )
        st.markdown("<br>", unsafe_allow_html=True)
    # ==============================================================

    folium.LayerControl(collapsed=False).add_to(fmap)
    
    return fmap
