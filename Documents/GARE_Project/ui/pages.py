import streamlit as st
from core.data import get_mineral, get_mineral_names, get_top_occurrences
from services.map import build_folium_map

def render_home():
    st.title("Material ID")
    st.markdown("""
        Welcome to **Material ID** — a mineral exploration assistant.
        - Search for a mineral by name.
        - Explore physical and geological information.
        - See real-world occurrences on an interactive map.
    """)
    st.markdown("---")
    st.subheader("Quick Selection")
    
    # Melhoria na grade de botões
    names = get_mineral_names()
    cols = st.columns(3)
    for i, mineral in enumerate(names):
        if cols[i % 3].button(mineral, key=f"btn_{mineral}"):
            st.session_state.selected_mineral = mineral
            st.session_state.page = "physical"
            st.rerun()

def render_physical(mineral_name: str):
    mineral = get_mineral(mineral_name)
    if not mineral:
        st.warning("Please select a mineral first.")
        return
    st.title(f"{mineral['name']} — Physical Properties")
    st.write(f"**Class:** {mineral.get('class', 'N/A')}")
    st.write(f"**Brightness:** {mineral.get('brightness', 'N/A')}")
    st.write(f"**Texture:** {mineral.get('texture', 'N/A')}")
    
    if st.button("Next: Geological Context"):
        st.session_state.page = "geological"
        st.rerun()

def render_geological(mineral_name: str):
    mineral = get_mineral(mineral_name)
    if not mineral: return
    st.title(f"{mineral['name']} — Geological Information")
    st.write(f"**Context:** {mineral.get('geological_context', 'N/A')}")
    
    if st.button("Next: Europe Map"):
        st.session_state.page = "map"
        st.rerun()

def render_map(mineral_name: str):
    from streamlit_folium import st_folium
    mineral = get_mineral(mineral_name)
    if not mineral: return
    st.title(f"{mineral['name']} — Distribution Map")
    
    occurrences = get_top_occurrences(mineral_name)
    map_obj = build_folium_map(occurrences)
    st_folium(map_obj, height=500, width=700)
    
    if st.button("Next: Quiz"):
        st.session_state.page = "quiz"
        st.rerun()

def render_quiz(mineral_name: str):
    from services.quiz import render_mineral_quiz
    st.title(f"Quiz: {mineral_name}")
    render_mineral_quiz(mineral_name)