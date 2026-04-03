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

def render_map(mineral_name, occurrences):
    import streamlit as st
    
    st.title("Geographical Distribution")
    st.subheader(f"Occurrences of {mineral_name}")
    
    # 1. Verifica se recebemos dados válidos
    if occurrences is None or len(occurrences) == 0:
        st.warning("No location data/coordinates available for this resource.")
        return

    # 2. Tenta desenhar o mapa
    try:
        from services.map import build_folium_map
        from streamlit_folium import st_folium
        
        map_obj = build_folium_map(occurrences)
        if map_obj:
            st_folium(map_obj, width=800, height=500)
        else:
            st.warning("Map could not be generated.")
            
    except Exception as e:
        # Se houver algum erro com o Folium, mostra os dados em tabela para não crashar a app
        st.error(f"Error loading the map module. Showing raw data instead.")
        st.dataframe(occurrences)
import streamlit as st

def render_quiz():
    st.title("🧠 Quiz de Conhecimentos Geológicos")
    st.markdown("Teste o que aprendeu ao explorar os mapas sobre o **Lítio** e o **Hidrogénio**!")

    # 1. As Perguntas (3 de Lítio, 3 de Hidrogénio)
    questions = {
        "Lítio": [
            {
                "pergunta": "1. Qual é a principal aplicação do Lítio hoje em dia?",
                "opcoes": ["Construção Civil", "Baterias de iões de lítio", "Joalharia", "Combustível para aviões"],
                "resposta": "Baterias de iões de lítio"
            },
            {
                "pergunta": "2. Em Portugal, o Lítio é encontrado frequentemente associado a que tipo de rocha?",
                "opcoes": ["Calcário", "Basalto", "Pegmatitos", "Areia da praia"],
                "resposta": "Pegmatitos"
            },
            {
                "pergunta": "3. Qual destas características torna o Lítio num elemento único?",
                "opcoes": ["É o metal mais leve que existe", "É magnético", "É líquido à temperatura ambiente", "Brilha no escuro"],
                "resposta": "É o metal mais leve que existe"
            }
        ],
        "Hidrogénio": [
            {
                "pergunta": "1. Como é frequentemente conhecido o hidrogénio gerado naturalmente na crosta terrestre?",
                "opcoes": ["Hidrogénio Verde", "Hidrogénio Branco (Geológico)", "Hidrogénio Cinzento", "Hidrogénio Azul"],
                "resposta": "Hidrogénio Branco (Geológico)"
            },
            {
                "pergunta": "2. O que torna o Hidrogénio tão interessante para o futuro da energia?",
                "opcoes": ["Quando 'queimado', só liberta vapor de água", "É muito fácil e barato de extrair", "Substitui o urânio nas centrais nucleares", "Não precisa de ser armazenado"],
                "resposta": "Quando 'queimado', só liberta vapor de água"
            },
            {
                "pergunta": "3. O Hidrogénio natural fica muitas vezes acumulado no subsolo em...",
                "opcoes": ["Lagos subterrâneos de água doce", "Bolsas e armadilhas geológicas (rochas porosas/falhas)", "Minas de carvão abandonadas", "Magma vulcânico"],
                "resposta": "Bolsas e armadilhas geológicas (rochas porosas/falhas)"
            }
        ]
    }

    # 2. Inicializar a memória do Streamlit para o Quiz
    if 'quiz_submetido' not in st.session_state:
        st.session_state.quiz_submetido = False
    if 'pontuacao' not in st.session_state:
        st.session_state.pontuacao = 0

    # 3. Lógica: Se o quiz ainda NÃO foi submetido, mostramos o formulário
    if not st.session_state.quiz_submetido:
        with st.form("quiz_form"):
            respostas_utilizador = {}
            
            st.subheader("⛏️ Secção 1: Lítio")
            for i, q in enumerate(questions["Lítio"]):
                respostas_utilizador[f"Li_{i}"] = st.radio(q["pergunta"], q["opcoes"], key=f"Li_{i}")
                st.write("---")

            st.subheader("💧 Secção 2: Hidrogénio")
            for i, q in enumerate(questions["Hidrogénio"]):
                respostas_utilizador[f"H_{i}"] = st.radio(q["pergunta"], q["opcoes"], key=f"H_{i}")
                st.write("---")

            # Botão mágico
            submit_button = st.form_submit_button("Submeter e Ver Resultados!")

            if submit_button:
                # Calcular pontuação
                score = 0
                for i, q in enumerate(questions["Lítio"]):
                    if respostas_utilizador[f"Li_{i}"] == q["resposta"]:
                        score += 1
                for i, q in enumerate(questions["Hidrogénio"]):
                    if respostas_utilizador[f"H_{i}"] == q["resposta"]:
                        score += 1
                
                # Guardar na memória e recarregar a página
                st.session_state.pontuacao = score
                st.session_state.quiz_submetido = True
                st.rerun()

    # 4. Lógica: Se o quiz JÁ foi submetido, mostramos a avaliação final
    else:
        total_perguntas = 6
        score = st.session_state.pontuacao
        
        st.header("🏆 Resultados do Quiz")
        st.write(f"### Acertaste em **{score}** de **{total_perguntas}** perguntas!")
        
        # A avaliação personalizada
        if score == 6:
            st.success("Perfeito! Foste um autêntico geólogo de elite! Prestaste muita atenção aos dados. Parabéns! 🎉")
            st.balloons() # Lança balões no ecrã!
        elif score >= 4:
            st.info("Muito bem! Tens bons conhecimentos, mas ainda deixaste escapar um ou outro detalhe. Bom trabalho! 👍")
        elif score >= 2:
            st.warning("Razoável... Parece que passaste os olhos pela informação muito rápido. Que tal dares mais uma vista de olhos na app? 📖")
        else:
            st.error("Ops! Claramente vieste só pelo passeio. Volta aos mapas e à informação antes de tentares outra vez! 😅")
        
        # Botão para recomeçar
        if st.button("Tentar Novamente"):
            st.session_state.quiz_submetido = False
            st.session_state.pontuacao = 0
            st.rerun()    
