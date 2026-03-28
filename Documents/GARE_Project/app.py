import streamlit as st
from core.data import get_mineral, get_mineral_names, load_data, mineral_exists, get_top_occurrences
from ui.pages import render_home, render_physical, render_geological, render_map, render_quiz

def main():
    # Configuração da Página
    st.set_page_config(page_title="Material ID - Geology Explorer", layout="wide")

    # Inicialização do estado da sessão para o mineral selecionado
    if 'selected_mineral' not in st.session_state:
        st.session_state['selected_mineral'] = None

    # --- SIDEBAR / NAVEGAÇÃO ---
    st.sidebar.title("Navigation")
    
    # Seletor de busca manual na sidebar
    search_query = st.sidebar.text_input("Search mineral", placeholder="e.g. Uranium")
    
    if search_query:
        if mineral_exists(search_query.capitalize()):
            st.session_state['selected_mineral'] = search_query.capitalize()
    
    # Menu de rádio para as páginas
    menu = st.sidebar.radio(
        "Go to",
        ["home", "physical", "geological", "map", "quiz"]
    )

    if st.sidebar.button("Clear selection"):
        st.session_state['selected_mineral'] = None
        st.rerun()

    # --- LÓGICA DE RENDERIZAÇÃO ---
    
    # 1. Carregamos o nome do mineral selecionado
    mineral_name = st.session_state['selected_mineral']
    
    # 2. Buscamos os dados completos desse mineral (se existir)
    mineral_data = None
    if mineral_name:
        mineral_data = get_mineral(mineral_name)

    # 3. Encaminhamento para as páginas
    if menu == "home":
        render_home()

    elif menu == "physical":
        if mineral_data:
            render_physical(mineral_data)
        else:
            st.warning("⚠️ Seleciona um mineral na Home primeiro!")

    elif menu == "geological":
        if mineral_data:
            render_geological(mineral_data)
        else:
            st.warning("⚠️ Seleciona um mineral na Home primeiro!")

    elif menu == "map":
        if mineral_name:
            # Pegamos as ocorrências para o mapa
            occurrences = get_top_occurrences(mineral_name)
            render_map(mineral_name, occurrences)
        else:
            st.warning("⚠️ Seleciona um mineral na Home primeiro!")

    elif menu == "quiz":
        if mineral_data:
            # CHAMADA CORRIGIDA: Agora passamos os dados que carregámos acima
            render_quiz(mineral_data)
        else:
            st.info("ℹ️ Para começar o Quiz, seleciona um recurso geológico na página Home.")

if __name__ == "__main__":
    main()