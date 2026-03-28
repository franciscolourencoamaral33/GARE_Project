import streamlit as st
from core.data import get_mineral, get_mineral_names, get_top_occurrences
from services.map import build_folium_map
from streamlit_folium import st_folium

def render_home():
    st.title("Material ID")
    st.markdown("Bem-vindo ao explorador de recursos geológicos.")
    st.markdown("---")
    st.subheader("Seleção Rápida (Base de Dados CSV)")
    
    names = get_mineral_names()
    cols = st.columns(3)
    for i, mineral in enumerate(names):
        # Cria botões dinamicamente com base no CSV
        if cols[i % 3].button(mineral, key=f"btn_{mineral}"):
            st.session_state.selected_mineral = mineral
            st.session_state.page = "physical"
            st.rerun()

def render_physical(mineral_name: str):
    mineral = get_mineral(mineral_name)
    if not mineral:
        st.warning("Selecione um mineral na Home.")
        return

    st.title(f"{mineral_name} — Propriedades e Localização")
    
    # Usando as colunas reais do teu CSV
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Dataset:** {mineral.get('Dataset', 'N/A')}")
        st.write(f"**País de Exemplo:** {mineral.get('Country', 'N/A')}")
    with col2:
        st.write(f"**Teor / Concentração:** {mineral.get('Grade / Concentration', 'N/A')}")
        st.write(f"**Status:** {mineral.get('Status', 'N/A')}")

    st.markdown("---")
    if st.button("Próximo: Contexto Geológico"):
        st.session_state.page = "geological"
        st.rerun()

def render_geological(mineral_name: str):
    mineral = get_mineral(mineral_name)
    if not mineral: return

    st.title(f"{mineral_name} — Contexto Geológico")
    
    st.success(f"**Geological Setting:** {mineral.get('Geological Setting', 'N/A')}")
    st.write(f"**Host Rock / Reservoir:** {mineral.get('Host Rock / Reservoir', 'N/A')}")
    st.write(f"**Tipo de Depósito:** {mineral.get('Deposit Type / Trap Type', 'N/A')}")
    st.write(f"**Notas:** {mineral.get('Notes', 'N/A')}")

    st.markdown("---")
    if st.button("Próximo: Ver no Mapa"):
        st.session_state.page = "map"
        st.rerun()

def render_map(mineral_name: str):
    st.title(f"Mapa de Ocorrências: {mineral_name}")
    
    occurrences = get_top_occurrences(mineral_name)
    
    # Criar o mapa usando a tua função de service
    map_obj = build_folium_map(occurrences)
    st_folium(map_obj, height=500, width=800)
    
    st.write(f"Encontradas {len(occurrences)} ocorrências no dataset.")