import streamlit as st
from core.data import mineral_exists
from ui.pages import render_home, render_physical, render_geological, render_map

# -----------------------------------------------------------------------------
# Styling helpers
# -----------------------------------------------------------------------------
def _inject_styles():
    st.markdown("""
        <style>
            .stSidebar { background-color: #f8f9fa; }
            .stSidebar [data-testid="stMarkdownContainer"] p {
                color: #1a1a1a !important;
                font-weight: 500;
            }
            div.stButton > button:first-child {
                background-color: #007bff;
                color: white;
                border-radius: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Session state helpers
# -----------------------------------------------------------------------------
def _init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "selected_mineral" not in st.session_state:
        st.session_state.selected_mineral = None
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""

def _set_selected_mineral(mineral_name: str):
    st.session_state.selected_mineral = mineral_name
    st.session_state.page = "physical"

def _search_and_select():
    query = st.session_state.search_query.strip()
    if not query:
        return
    if not mineral_exists(query):
        st.sidebar.error("Mineral not found.")
        return
    _set_selected_mineral(query)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="Material ID", layout="wide")
    _init_session_state()
    _inject_styles()

    st.sidebar.title("Mineral Search")

    st.sidebar.text_input(
        "Search mineral",
        key="search_query",
        placeholder="e.g. Quartz",
        on_change=_search_and_select,
    )

    st.sidebar.markdown("---")

    # SOLUÇÃO PARA O ERRO: Usar uma chave diferente para o widget
    pages = ["home", "physical", "geological", "map", "quiz"]
    
    # Se o utilizador mudar o rádio, atualizamos o state da página
    def sync_page():
        st.session_state.page = st.session_state.nav_radio

    st.sidebar.radio(
        "Navigation",
        options=pages,
        index=pages.index(st.session_state.page),
        key="nav_radio",
        on_change=sync_page
    )

    if st.sidebar.button("Clear selection"):
        st.session_state.selected_mineral = None
        st.session_state.page = "home"
        st.rerun()

    # Renderização baseada no state
    current_page = st.session_state.page
    mineral = st.session_state.selected_mineral or ""

    if current_page == "home":
        render_home()
    elif current_page == "physical":
        render_physical(mineral)
    elif current_page == "geological":
        render_geological(mineral)
    elif current_page == "map":
        render_map(mineral)
    elif current_page == "quiz":
        render_quiz(mineral)

if __name__ == "__main__":
    main()
