import folium
from folium.plugins import MarkerCluster
import pandas as pd

def build_folium_map(occurrences):
    # 1. Adaptar os dados (funciona quer venha do Pandas DataFrame ou lista)
    if isinstance(occurrences, pd.DataFrame):
        data_points = occurrences.to_dict('records')
    else:
        data_points = occurrences

    # 2. Filtrar apenas as linhas que tenham Latitude e Longitude válidas
    valid_points = []
    for point in data_points:
        try:
            lat = float(point.get("Latitude", ""))
            lon = float(point.get("Longitude", ""))
            valid_points.append({"lat": lat, "lon": lon, "data": point})
        except (ValueError, TypeError):
            continue

    # 3. Se não houver dados válidos, mostra um mapa vazio centrado na Europa
    if not valid_points:
        return folium.Map(location=[39.5, 15.0], zoom_start=4, tiles="CartoDB positron")

    # 4. Calcular o centro do mapa com base na média dos pontos
    avg_lat = sum(p["lat"] for p in valid_points) / len(valid_points)
    avg_lon = sum(p["lon"] for p in valid_points) / len(valid_points)

    fmap = folium.Map(
        location=[avg_lat, avg_lon],
        zoom_start=4,
        tiles="CartoDB positron"
    )

    # 5. Cluster de marcadores inspirado no código do teu colega
    cluster = MarkerCluster(name="Ocorrências").add_to(fmap)

    # 6. Desenhar cada ponto válido
    for p in valid_points:
        row = p["data"]
        name = str(row.get("Name", "Desconhecido")).strip()
        country = str(row.get("Country", "Desconhecido")).strip()
        resource = str(row.get("Resource", "Sem recurso")).strip()
        
        # Um popup limpo para não sobrecarregar o mapa
        popup_html = f"""
        <div style='min-width:200px; font-family: sans-serif;'>
            <b>Resource:</b> {resource}<br>
            <b>Name:</b> {name}<br>
            <b>Country:</b> {country}
        </div>
        """

        folium.CircleMarker(
            location=[p["lat"], p["lon"]],
            radius=6,
            color="#1f77b4", # Azul da paleta do teu colega
            weight=1,
            fill=True,
            fill_color="#1f77b4",
            fill_opacity=0.85,
            tooltip=f"{name} | {country}",
            popup=folium.Popup(popup_html, max_width=300),
        ).add_to(cluster)

    return fmap
