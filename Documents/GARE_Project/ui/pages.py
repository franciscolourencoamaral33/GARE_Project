import streamlit as st
from core.data import get_mineral, get_mineral_names, get_top_occurrences
from services.map import build_folium_map
from streamlit_folium import st_folium

def render_home():
    from core.data import get_mineral_names
    import streamlit as st

    st.title("Material ID - Geology Explorer")
    st.write("Select a mineral resource to explore its properties, geological setting, and location.")

    # 1. Vai buscar os nomes reais do teu ficheiro CSV
    names = get_mineral_names()

    if not names:
        st.warning("No minerals found in the database. Check your CSV file.")
        return

    # 2. Cria os botões dinamicamente
    cols = st.columns(3)
    for i, name in enumerate(names):
        with cols[i % 3]:
            # Se o botão for clicado:
            if st.button(name, key=f"btn_{name}", use_container_width=True):
                st.session_state['selected_mineral'] = name
                st.session_state['menu_option'] = "physical" # Faz o salto de página
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

def render_quiz(mineral_name: str):
    st.title(f"Quiz Geológico: {mineral_name if mineral_name else 'Geral'}")
    st.write("Testa os teus conhecimentos sobre este recurso!")
    
    # Exemplo de uma pergunta simples
    pergunta = f"O recurso {mineral_name} é considerado um recurso renovável?"
    opcao = st.radio(pergunta, ["Sim", "Não", "Depende da exploração"])
    
    if st.button("Submeter Resposta"):
        if opcao == "Não":
            st.success("Correto! Recursos minerais e fósseis são não-renováveis à escala humana.")
        else:
            st.error("Incorreto. Tenta rever a seção de Contexto Geológico.")    
