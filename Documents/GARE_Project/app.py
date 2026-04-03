import streamlit as st
from core.data import get_mineral, get_mineral_names, load_data, mineral_exists, get_top_occurrences
from ui.pages import render_home, render_physical, render_geological, render_map, render_quiz

def main():
    st.set_page_config(page_title="Material ID - Geology Explorer", layout="wide")

    # 1. INICIALIZAÇÃO DE ESTADOS
    if 'menu_option' not in st.session_state:
        st.session_state['menu_option'] = "home"
    
    if 'selected_mineral' not in st.session_state:
        st.session_state['selected_mineral'] = None

    # 2. SIDEBAR
    st.sidebar.title("Navigation")
    
    search_query = st.sidebar.text_input("🔍 Search mineral", placeholder="e.g. Orthoclase")
    if search_query:
        # Se a pessoa pesquisar, guarda e vai para as propriedades
        st.session_state['selected_mineral'] = search_query.capitalize()
        st.session_state['menu_option'] = "physical"

    options = ["home", "physical", "geological", "map", "quiz"]
    
    # Descobre qual é a página que devia estar selecionada
    try:
        current_index = options.index(st.session_state['menu_option'])
    except ValueError:
        current_index = 0

    # O MENU: Sem o parâmetro "key" que causou o erro! Usamos apenas o index.
    menu = st.sidebar.radio(
        "Go to",
        options,
        index=current_index
    )

    # Se o utilizador clicou no menu lateral com o rato, atualiza a app
    if menu != st.session_state['menu_option']:
        st.session_state['menu_option'] = menu
        st.rerun()

    if st.sidebar.button("Clear selection"):
        st.session_state['selected_mineral'] = None
        st.session_state['menu_option'] = "home"
        st.rerun()

    # 3. RENDERIZAÇÃO DAS PÁGINAS COM SEGURANÇA
    mineral_name = st.session_state['selected_mineral']

    if st.session_state['menu_option'] == "home":
        render_home()
        
    elif st.session_state['menu_option'] == "physical":
        data = get_mineral(mineral_name) if mineral_name else None
        if data is not None:
            render_physical(data)
        else:
            st.warning("👈 Por favor, seleciona um mineral na Home primeiro para ver as propriedades.")
            
    elif st.session_state['menu_option'] == "geological":
        data = get_mineral(mineral_name) if mineral_name else None
        if data is not None:
            render_geological(data)
        else:
            st.warning("👈 Por favor, seleciona um mineral na Home primeiro.")
            
    elif st.session_state['menu_option'] == "map":
        occurrences = get_top_occurrences(mineral_name) if mineral_name else []
        if occurrences:
            render_map(mineral_name, occurrences)
        else:
            st.warning("👈 Nenhum dado de localização encontrado. Seleciona um mineral na Home primeiro.")
            
    elif st.session_state['menu_option'] == "quiz":
        data = get_mineral(mineral_name) if mineral_name else None
        if data is not None:
            render_quiz(data)
        else:
            st.warning("👈 Por favor, seleciona um mineral na Home primeiro para iniciar o Quiz.")

if __name__ == "__main__":
    main()
