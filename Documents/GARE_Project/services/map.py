import folium


def build_folium_map(occurrences: list, start_zoom=4, start_location=(54.0, 10.0)) -> folium.Map:
    """Build and return a folium Map with markers for each occurrence."""

    # Compute centroid based on occurrences if available
    if occurrences:
        avg_lat = sum(o.get("lat", 0) for o in occurrences) / len(occurrences)
        avg_lon = sum(o.get("lon", 0) for o in occurrences) / len(occurrences)
        start_location = (avg_lat, avg_lon)

    m = folium.Map(location=start_location, zoom_start=start_zoom, tiles="OpenStreetMap")

    for occ in occurrences:
        lat = occ.get("lat")
        lon = occ.get("lon")
        if lat is None or lon is None:
            continue

        score = occ.get("score", 0)
        color = "green" if score >= 80 else "orange" if score >= 60 else "red"

        popup_html = f"<b>{occ.get('country', 'Unknown')}</b><br/>" \
            f"{occ.get('region', 'Unknown')}<br/>" \
            f"Type: {occ.get('type', 'Unknown')}<br/>" \
            f"Score: {score}/100"

        folium.CircleMarker(
            location=(lat, lon),
            radius=8,
            color="#333",
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(m)

    return m
