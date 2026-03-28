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
    mineral = st.session_state['selected_mineral']

    if menu == "home":
        render_home()
    elif menu == "physical":
        render_physical(mineral)
    elif menu == "geological":
        render_geological(mineral)
    elif menu == "map":
        render_map(mineral)
    elif menu == "quiz":
        render_quiz(mineral)

if __name__ == "__main__":
    main()