import streamlit as st
from core.data import mineral_exists
from ui.pages import render_home, render_physical, render_geological, render_map, render_quiz

def main():
    st.set_page_config(page_title="Material ID - Geology Explorer", layout="wide")

    if 'selected_mineral' not in st.session_state:
        st.session_state['selected_mineral'] = None

    # Sidebar
    st.sidebar.title("Navigation")
    
    search_query = st.sidebar.text_input("Search mineral", placeholder="e.g. Quartz")
    
    if search_query:
        if mineral_exists(search_query.capitalize()):
            st.session_state['selected_mineral'] = search_query.capitalize()
    
    menu = st.sidebar.radio(
        "Navigation",
        ["home", "physical", "geological", "map", "quiz"]
    )

    if st.sidebar.button("Clear selection"):
        st.session_state['selected_mineral'] = None
        st.rerun()

    # Mineral selecionado
    mineral_name = st.session_state['selected_mineral']

    if menu == "home":
        # BUSCAMOS OS NOMES PARA OS BOTÕES APARECEREM
        names = get_mineral_names() 
        render_home(names) # Passamos a lista de nomes aqui
    
    elif menu == "physical":
        data = get_mineral(mineral_name) if mineral_name else None
        render_physical(data)
        
    elif menu == "geological":
        data = get_mineral(mineral_name) if mineral_name else None
        render_geological(data)
        
    elif menu == "map":
        occurrences = get_top_occurrences(mineral_name) if mineral_name else []
        render_map(mineral_name, occurrences)
        
    elif menu == "quiz":
        data = get_mineral(mineral_name) if mineral_name else None
        render_quiz(data)

if __name__ == "__main__":
    main()
