import folium
from folium.plugins import MarkerCluster
import pandas as pd
import html
import math

# Paleta de cores do teu colega
PALETTE = [
    "#1f77b4", "#d62728", "#2ca02c", "#ff7f0e",
    "#9467bd", "#8c564b", "#17becf",
]

# Campos que aparecem na janela ao clicar na bolinha
POPUP_FIELDS = [
    "Dataset", "Resource", "Name", "Country", "Geological Setting",
    "Host Rock / Reservoir", "Deposit Type / Trap Type",
    "Grade / Concentration", "Size / Reserves", "Depth",
    "Temperature", "Status", "Notes"
]

def build_popup(row):
    """Constrói a tabela HTML igual à do script original."""
    lines = []
    for field in POPUP_FIELDS:
        value = str(row.get(field, "")).strip()
        # Ignora campos vazios ou 'nan'/'none'
        if not value or value.lower() in ('nan', 'none'):
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

def build_legend(categories, color_map):
    """Constrói a legenda flutuante no canto inferior do mapa."""
    items = []
    for cat in categories:
        color = color_map[cat]
        items.append(
            "<div style='display:flex; align-items:center; margin-bottom:6px;'>"
            f"<span style='display:inline-block; width:12px; height:12px; "
            f"background:{color}; border-radius:50%; margin-right:8px;'></span>"
            f"<span>{html.escape(cat)}</span>"
            "</div>"
        )

    return (
        "<div style='position: fixed; bottom: 20px; left: 20px; z-index: 9999; "
        "background: white; padding: 12px 14px; border: 1px solid #ccc; "
        "border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); "
        "font-family: Arial, sans-serif; font-size: 13px;'>"
        "<div style='font-weight:700; margin-bottom:8px;'>Legenda (País)</div>"
        + "".join(items)
        + "</div>"
    )

def build_folium_map(occurrences):
    """Função principal que desenha o mapa a partir dos dados do Streamlit."""
    # 1. Tratar os dados que vêm do Pandas, trocando NaNs por strings vazias
    if isinstance(occurrences, pd.DataFrame):
        occurrences = occurrences.fillna("")
        data_points = occurrences.to_dict('records')
    else:
        data_points = occurrences

    # 2. Filtragem rigorosa de coordenadas
    valid_points = []
    for point in data_points:
        lat_raw = str(point.get("Latitude", "")).replace(",", ".")
        lon_raw = str(point.get("Longitude", "")).replace(",", ".")
        
        try:
            # Se a string estiver vazia ou for literalmente "none"/"nan", salta
            if not lat_raw or not lon_raw or lat_raw.lower() in ('nan', 'none') or lon_raw.lower() in ('nan', 'none'):
                continue
                
            lat = float(lat_raw)
            lon = float(lon_raw)
            
            # Verificação matemática extra contra erros invisíveis
            if math.isnan(lat) or math.isnan(lon):
                continue
                
            valid_points.append({"lat": lat, "lon": lon, "data": point})
        except (ValueError, TypeError):
            continue

    # 3. Fallback se nenhum ponto tiver coordenadas
    if not valid_points:
        return folium.Map(location=[39.5, 15.0], zoom_start=4, tiles="CartoDB positron")

    # 4. Centralizar o mapa
    avg_lat = sum(p["lat"] for p in valid_points) / len(valid_points)
    avg_lon = sum(p["lon"] for p in valid_points) / len(valid_points)

    fmap = folium.Map(location=[avg_lat, avg_lon], zoom_start=4, tiles="CartoDB positron")

    # 5. Criar Categorias por País (como sugeriste) e as respetivas cores
    categories = sorted({str(p["data"].get("Country", "Desconhecido")).strip() or "Desconhecido" for p in valid_points})
    color_map = {cat: PALETTE[index % len(PALETTE)] for index, cat in enumerate(categories)}
    clusters = {}

    # 6. Adicionar os Layers (Grupos) por país ao mapa
    for cat in categories:
        group = folium.FeatureGroup(name=cat, show=True).add_to(fmap)
        clusters[cat] = MarkerCluster(name=f"{cat} cluster").add_to(group)

    # 7. Adicionar cada marcador com o PopUp
    for p in valid_points:
        row = p["data"]
        cat = str(row.get("Country", "Desconhecido")).strip() or "Desconhecido"
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

    # 8. Renderizar a Legenda
    if categories:
        legend_html = build_legend(categories, color_map)
        fmap.get_root().html.add_child(folium.Element(legend_html))

    # Controlos de Layer (para poder ligar/desligar países)
    folium.LayerControl(collapsed=False).add_to(fmap)
    
    return fmap
