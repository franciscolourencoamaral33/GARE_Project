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
                
def render_physical(data):
    import streamlit as st
    st.title("Physical & General Properties")
    
    if not data:
        st.warning("No data available for this mineral.")
        return

    # Usamos data.get('NomeDaColuna', 'Texto alternativo se não existir')
    st.subheader(f"Resource: {data.get('Resource', 'Unknown')}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Specific Name/Location:** {data.get('Name', 'N/A')}")
        st.write(f"**Country:** {data.get('Country', 'N/A')}")
        st.write(f"**Status:** {data.get('Status', 'N/A')}")
    
    with col2:
        st.write(f"**Grade / Concentration:** {data.get('Grade / Concentration', 'N/A')}")
        st.write(f"**Size / Reserves:** {data.get('Size / Reserves', 'N/A')}")
        
    st.write("---")
    st.write(f"**Notes:** {data.get('Notes', 'N/A')}")
    st.write(f"**Source:** {data.get('Source', 'N/A')}")


def render_geological(data):
    import streamlit as st
    st.title("Geological Setting")
    
    if not data:
        st.warning("No data available for this mineral.")
        return

    st.write(f"**Geological Setting:** {data.get('Geological Setting', 'N/A')}")
    st.write(f"**Host Rock / Reservoir:** {data.get('Host Rock / Reservoir', 'N/A')}")
    st.write(f"**Deposit Type / Trap Type:** {data.get('Deposit Type / Trap Type', 'N/A')}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Depth:** {data.get('Depth', 'N/A')}")
    with col2:
        st.write(f"**Temperature:** {data.get('Temperature', 'N/A')}")

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
