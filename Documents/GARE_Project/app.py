import streamlit as st
from core.data import get_mineral, get_mineral_names, load_data, mineral_exists, get_top_occurrences
from ui.pages import render_home, render_physical, render_geological, render_map, render_quiz

def main():
    st.set_page_config(page_title="Material ID - Geology Explorer", layout="wide")

    # 1. INICIALIZAÇÃO DE ESTADOS (Crucial para a navegação)
    if 'menu_option' not in st.session_state:
        st.session_state['menu_option'] = "home"
    
    if 'selected_mineral' not in st.session_state:
        st.session_state['selected_mineral'] = None

    # 2. SIDEBAR E NAVEGAÇÃO
    st.sidebar.title("Navigation")
    
    # Campo de pesquisa
    search_query = st.sidebar.text_input("Search mineral", placeholder="e.g. Orthoclase")
    if search_query:
        if mineral_exists(search_query):
            st.session_state['selected_mineral'] = search_query
            st.session_state['menu_option'] = "physical" # Salta para detalhes ao pesquisar

    # Configuração do Rádio sincronizado com o clique dos botões
    options = ["home", "physical", "geological", "map", "quiz"]
    
    # Descobre em que posição da lista está a página atual
    try:
        current_index = options.index(st.session_state['menu_option'])
    except ValueError:
        current_index = 0

    menu = st.sidebar.radio(
        "Go to",
        options,
        index=current_index,
        key="navigation_menu"
    )

    # Se o utilizador clicar manualmente no rádio, atualizamos o estado
    if menu != st.session_state['menu_option']:
        st.session_state['menu_option'] = menu

    if st.sidebar.button("Clear selection"):
        st.session_state['selected_mineral'] = None
        st.session_state['menu_option'] = "home"
        st.rerun()

    # 3. RENDERIZAÇÃO DAS PÁGINAS
    mineral_name = st.session_state['selected_mineral']

    if st.session_state['menu_option'] == "home":
        render_home()
    elif st.session_state['menu_option'] == "physical":
        data = get_mineral(mineral_name) if mineral_name else None
        render_physical(data)
    elif st.session_state['menu_option'] == "geological":
        data = get_mineral(mineral_name) if mineral_name else None
        render_geological(data)
    elif st.session_state['menu_option'] == "map":
        occurrences = get_top_occurrences(mineral_name) if mineral_name else []
        render_map(mineral_name, occurrences)
    elif st.session_state['menu_option'] == "quiz":
        data = get_mineral(mineral_name) if mineral_name else None
        render_quiz(data)

if __name__ == "__main__":
    main()
