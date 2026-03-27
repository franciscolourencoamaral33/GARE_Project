import streamlit as st
from core.data import get_mineral, get_mineral_names, get_top_occurrences
from services.map import build_folium_map


def render_home():
    st.title("Material ID")
    st.markdown(
        """
        Welcome to **Material ID** — a mineral exploration assistant.

        - Search for a mineral by name.
        - Explore physical and geological information.
        - See real-world occurrences on an interactive map.
        """
    )

    st.markdown("---")

    st.subheader("Quick Selection")
    cols = st.columns(3)
    for i, mineral in enumerate(get_mineral_names()):
        if cols[i].button(mineral):
            st.session_state.selected_mineral = mineral
            st.session_state.page = "physical"
            st.rerun()


def render_physical(mineral_name: str):
    mineral = get_mineral(mineral_name)
    if not mineral:
        st.error("No mineral selected. Choose one from the sidebar or search first.")
        return

    st.title(f"{mineral.get('name', '')} — Physical Properties")

    st.markdown(
        f"""
        **Mineral class:** {mineral.get('class', 'Unknown')}  
        **Brightness:** {mineral.get('brightness', 'Unknown')}  
        **Texture:** {mineral.get('texture', 'Unknown')}  
        **Extra:** {mineral.get('extra_characteristics', 'N/A')}
        """
    )

    st.markdown("---")
    st.button("Next: Geological Context", key="next_geo", on_click=lambda: st.session_state.update({"page": "geological"}))


def render_geological(mineral_name: str):
    mineral = get_mineral(mineral_name)
    if not mineral:
        st.error("No mineral selected. Choose one from the sidebar or search first.")
        return

    st.title(f"{mineral.get('name', '')} — Geological Information")

    st.markdown(
        f"""
        **Geological context:** {mineral.get('geological_context', 'N/A')}  
        **Deposit type:** {mineral.get('deposit_type', 'N/A')}  
        **Tectonic context:** {mineral.get('tectonic_context', 'N/A')}
        """
    )

    st.markdown("---")
    st.button("Next: Europe Map", key="next_map", on_click=lambda: st.session_state.update({"page": "map"}))


def render_map(mineral_name: str):
    mineral = get_mineral(mineral_name)
    if not mineral:
        st.error("No mineral selected. Choose one from the sidebar or search first.")
        return

    st.title(f"{mineral.get('name', mineral_name)} — Europe Map")

    occurrences = get_top_occurrences(mineral_name, limit=10)
    if not occurrences:
        st.warning("No occurrence data available for this mineral.")
        return

    from streamlit_folium import st_folium

    map_obj = build_folium_map(occurrences)
    st_folium(map_obj, height=600, width=800)

    st.markdown("---")
    st.subheader("Top occurrences")
    for occ in occurrences:
        st.markdown(
            f"**{occ['country']}** — {occ['region']}  \nType: {occ['type']} • Score: {occ['score']}"
        )

    st.markdown("---")
    st.button("Next: Quiz", key="next_quiz", on_click=lambda: st.session_state.update({"page": "quiz"}))


def render_quiz(mineral_name: str):
    mineral = get_mineral(mineral_name)
    if not mineral:
        st.error("No mineral selected. Choose one from the sidebar or search first.")
        return

    # Provide context so the user knows this is a quiz section
    st.title(f"{mineral.get('name', mineral_name)} — Quiz")
    st.markdown(
        """
        Test your knowledge with a short quiz about this mineral.

        Answer the questions below and click **Submit Quiz** to see your score.
        """
    )

    from services.quiz import render_mineral_quiz

    render_mineral_quiz(mineral_name)
