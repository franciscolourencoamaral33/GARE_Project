import streamlit as st

from core.data import mineral_exists
from ui.pages import render_home, render_physical, render_geological, render_map, render_quiz


# -----------------------------------------------------------------------------
# Styling helpers
# -----------------------------------------------------------------------------

def _inject_styles():
    st.markdown(
        """
        <style>
        .reportview-container {
            background: #FFFFFF;
        }
        .stSidebar {
            background: #F7F9FB;
        }
        .stButton>button {
            background-color: #87CEEB;
            color: #000000;
            border: 1px solid rgba(0,0,0,0.12);
        }
        .stButton>button:hover {
            background-color: #6ec6e0;
        }
        .stTextInput>div>div>input {
            border: 1px solid rgba(0,0,0,0.2);
        }
        .stMarkdown h1 {
            font-family: Montserrat, system-ui, sans-serif;
        }
        .stMarkdown h2 {
            font-family: Montserrat, system-ui, sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
        st.warning("Please enter a mineral name to search.")
        return

    if not mineral_exists(query):
        st.error("Mineral not found. Try Quartz, Feldspar, or Mica.")
        return

    _set_selected_mineral(query)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="Material ID", layout="wide")

    _inject_styles()
    _init_session_state()

    st.sidebar.title("Mineral Search")

    st.sidebar.text_input(
        "Search mineral",
        key="search_query",
        placeholder="e.g. Quartz",
        on_change=_search_and_select,
    )

    st.sidebar.markdown("---")

    st.sidebar.radio(
        "Navigation",
        options=["home", "physical", "geological", "map", "quiz"],
        index=["home", "physical", "geological", "map", "quiz"].index(
            st.session_state.page
        ),
        key="page",
    )

    if st.sidebar.button("Clear selection"):
        st.session_state.selected_mineral = None
        st.session_state.page = "home"

    if st.session_state.page == "home":
        render_home()
    elif st.session_state.page == "physical":
        render_physical(st.session_state.selected_mineral or "")
    elif st.session_state.page == "geological":
        render_geological(st.session_state.selected_mineral or "")
    elif st.session_state.page == "map":
        render_map(st.session_state.selected_mineral or "")
    elif st.session_state.page == "quiz":
        render_quiz(st.session_state.selected_mineral or "")


if __name__ == "__main__":
    main()
