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
        

def render_quiz(data):
    # 1. Descobrir qual é o mineral selecionado
    mineral_name = st.session_state.get('selected_mineral', 'Desconhecido')
    
    st.title(f"🧠 Quiz de Conhecimentos: {mineral_name}")
    st.markdown(f"Teste o que aprendeu ao explorar os dados sobre **{mineral_name}**!")

    # 2. Base de dados de perguntas (3 por mineral)
    questions_db = {
        "Lithium": [ # Substitui pela forma como está escrito no teu CSV (ex: "Lítio" se for em PT)
            {
                "pergunta": "1. Qual é a principal aplicação deste recurso hoje em dia?",
                "opcoes": ["Construção Civil", "Baterias de iões de lítio", "Joalharia", "Combustível para aviões"],
                "resposta": "Baterias de iões de lítio"
            },
            {
                "pergunta": "2. Em Portugal, este recurso é frequentemente encontrado associado a que tipo de rocha?",
                "opcoes": ["Calcário", "Basalto", "Pegmatitos", "Areia da praia"],
                "resposta": "Pegmatitos"
            },
            {
                "pergunta": "3. Qual destas características torna este elemento único?",
                "opcoes": ["É o metal mais leve que existe", "É magnético", "É líquido à temperatura ambiente", "Brilha no escuro"],
                "resposta": "É o metal mais leve que existe"
            }
        ],
        "Hydrogen": [ # Substitui pela forma como está escrito no teu CSV (ex: "Hidrogénio" se for em PT)
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
                "pergunta": "3. Onde fica muitas vezes acumulado no subsolo?",
                "opcoes": ["Lagos subterrâneos de água doce", "Bolsas e armadilhas geológicas", "Minas de carvão abandonadas", "Magma vulcânico"],
                "resposta": "Bolsas e armadilhas geológicas"
            }
        ]
    }

    # 3. Escolher o quiz certo com base no mineral escolhido
    quiz_atual = None
    for key in questions_db.keys():
        if key.lower() in mineral_name.lower() or mineral_name.lower() in key.lower():
            quiz_atual = questions_db[key]
            break
            
    # Se escolhermos um mineral que ainda não tem perguntas
    if not quiz_atual:
        st.info(f"🚧 O quiz para **{mineral_name}** ainda está em construção! Tenta selecionar Lithium ou Hydrogen na Home.")
        return

    # Criamos um "prefixo" para as chaves ser ÚNICAS para cada mineral (isto resolve o erro DuplicateWidgetID)
    prefix = mineral_name.replace(" ", "_")
    estado_quiz = f'quiz_subm_{prefix}'
    estado_pontuacao = f'pontos_{prefix}'

    # 4. Inicializar a memória do Streamlit
    if estado_quiz not in st.session_state:
        st.session_state[estado_quiz] = False
    if estado_pontuacao not in st.session_state:
        st.session_state[estado_pontuacao] = 0

    # 5. Mostrar formulário de 3 perguntas
    if not st.session_state[estado_quiz]:
        with st.form(f"form_quiz_{prefix}"):
            respostas_utilizador = {}
            
            for i, q in enumerate(quiz_atual):
                chave_unica = f"pergunta_{prefix}_{i}"
                respostas_utilizador[chave_unica] = st.radio(q["pergunta"], q["opcoes"], key=chave_unica)
                st.write("---")

            submit_button = st.form_submit_button("Submeter e Ver Resultados!")

            if submit_button:
                score = 0
                for i, q in enumerate(quiz_atual):
                    chave_unica = f"pergunta_{prefix}_{i}"
                    if respostas_utilizador[chave_unica] == q["resposta"]:
                        score += 1
                
                st.session_state[estado_pontuacao] = score
                st.session_state[estado_quiz] = True
                st.rerun()

    # 6. Avaliação Final (de 0 a 3 valores)
    else:
        total_perguntas = 3
        score = st.session_state[estado_pontuacao]
        
        st.header("🏆 Resultados do Quiz")
        st.write(f"### Acertaste em **{score}** de **{total_perguntas}** perguntas sobre {mineral_name}!")
        
        if score == 3:
            st.success("Perfeito! Foste um autêntico geólogo de elite! Prestaste muita atenção aos dados. Parabéns! 🎉")
            st.balloons()
        elif score == 2:
            st.info("Muito bem! Tens bons conhecimentos, mas ainda deixaste escapar um detalhe. Bom trabalho! 👍")
        elif score == 1:
            st.warning("Razoável... Passaste os olhos pela informação muito rápido. Que tal dares mais uma vista de olhos na app? 📖")
        else:
            st.error("Ops! Claramente vieste só pelo passeio. Volta aos mapas e à informação antes de tentares outra vez! 😅")
        
        if st.button("Tentar Novamente", key=f"btn_reset_{prefix}"):
            st.session_state[estado_quiz] = False
            st.session_state[estado_pontuacao] = 0
            st.rerun()
