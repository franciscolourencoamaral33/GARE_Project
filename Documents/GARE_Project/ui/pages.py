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

   # 2. Base de dados de perguntas (3 por recurso)
    questions_db = {
        "Lithium": [
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
        "Hydrogen": [
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
        ],
        "Cobalt": [
            {
                "pergunta": "1. Qual é a principal função do Cobalto nas tecnologias modernas?",
                "opcoes": ["Fazer vidro à prova de bala", "Estabilizar baterias recarregáveis", "Construir painéis solares", "Filtrar água potável"],
                "resposta": "Estabilizar baterias recarregáveis"
            },
            {
                "pergunta": "2. Qual é o país responsável pela maior parte da extração mundial de Cobalto?",
                "opcoes": ["Austrália", "Canadá", "República Democrática do Congo", "Rússia"],
                "resposta": "República Democrática do Congo"
            },
            {
                "pergunta": "3. Na mineração, o Cobalto é maioritariamente extraído como um subproduto de quais minérios?",
                "opcoes": ["Cobre e Níquel", "Ouro e Prata", "Ferro e Carvão", "Urânio e Chumbo"],
                "resposta": "Cobre e Níquel"
            }
        ],
        "Copper": [
            {
                "pergunta": "1. Qual é a principal propriedade física que torna o Cobre vital para a eletrificação?",
                "opcoes": ["É transparente", "É um excelente condutor de eletricidade e calor", "É mais duro que o diamante", "É altamente radioativo"],
                "resposta": "É um excelente condutor de eletricidade e calor"
            },
            {
                "pergunta": "2. Que cor adquire o cobre quando fica exposto aos elementos e oxida ao longo do tempo?",
                "opcoes": ["Preto", "Branco brilhante", "Verde (Verdete)", "Vermelho vivo"],
                "resposta": "Verde (Verdete)"
            },
            {
                "pergunta": "3. Qual é o tipo de depósito geológico que fornece a maior parte do cobre a nível mundial?",
                "opcoes": ["Pórfiro cuprífero (Porphyry)", "Placers de rio", "Veios de quartzo puro", "Rochas calcárias"],
                "resposta": "Pórfiro cuprífero (Porphyry)"
            }
        ],
        "Iridium": [
            {
                "pergunta": "1. O Irídio é famoso na geologia por estar concentrado numa camada de argila associada a que evento histórico?",
                "opcoes": ["A extinção dos dinossauros (limite K-Pg)", "A Idade do Gelo", "A formação do Oceano Atlântico", "A erupção do Monte Vesúvio"],
                "resposta": "A extinção dos dinossauros (limite K-Pg)"
            },
            {
                "pergunta": "2. O Irídio faz parte de que grupo restrito de metais na tabela periódica?",
                "opcoes": ["Metais Alcalinos", "Grupo da Platina (PGE)", "Terras Raras", "Halogéneos"],
                "resposta": "Grupo da Platina (PGE)"
            },
            {
                "pergunta": "3. Qual é uma das suas características físicas mais notáveis?",
                "opcoes": ["Flutua na água", "É extremamente tóxico", "É um dos metais mais densos e resistentes à corrosão do mundo", "Derrete com o calor das mãos"],
                "resposta": "É um dos metais mais densos e resistentes à corrosão do mundo"
            }
        ],
        "Nickel": [
            {
                "pergunta": "1. Qual tem sido, historicamente, a principal aplicação industrial do Níquel?",
                "opcoes": ["Ligas de Aço Inoxidável", "Produção de explosivos", "Fertilizantes agrícolas", "Vidro colorido"],
                "resposta": "Ligas de Aço Inoxidável"
            },
            {
                "pergunta": "2. O Níquel é frequentemente encontrado em grande abundância em que tipo de objetos extraterrestres?",
                "opcoes": ["Cometas de gelo", "Meteoritos metálicos (Ferro-Níquel)", "Poeira lunar", "Anéis de Saturno"],
                "resposta": "Meteoritos metálicos (Ferro-Níquel)"
            },
            {
                "pergunta": "3. Porque é que a procura de Níquel disparou recentemente?",
                "opcoes": ["Uso em reatores de fusão", "É um componente essencial nas baterias de veículos elétricos", "Substituição do cimento na construção civil", "Uso em ecrãs de telemóvel"],
                "resposta": "É um componente essencial nas baterias de veículos elétricos"
            }
        ],
        "Platinum": [
            {
                "pergunta": "1. Qual é a principal utilização da Platina na indústria automóvel (especialmente a combustão)?",
                "opcoes": ["Jantes de liga leve", "Conversores catalíticos (Catalisadores)", "Baterias de chumbo", "Velas de ignição"],
                "resposta": "Conversores catalíticos (Catalisadores)"
            },
            {
                "pergunta": "2. Qual é a região/país que abriga o Complexo de Bushveld, de onde vem a vasta maioria da Platina mundial?",
                "opcoes": ["Austrália", "Rússia", "África do Sul", "Brasil"],
                "resposta": "África do Sul"
            },
            {
                "pergunta": "3. Em química e medicina, a Platina é conhecida por...",
                "opcoes": ["Ser um excelente catalisador e não reagir facilmente", "Evaporar rapidamente", "Criar campos magnéticos fortes", "Ser muito radioativa"],
                "resposta": "Ser um excelente catalisador e não reagir facilmente"
            }
        ],
        "Rare Earth Elements": [
            {
                "pergunta": "1. Apesar do nome 'Terras Raras', qual é a verdade sobre a sua abundância na crosta terrestre?",
                "opcoes": ["Não existem, são criadas em laboratório", "São mais raras que o ouro e o ródio juntos", "São relativamente abundantes, mas raramente se encontram concentradas o suficiente para mineração rentável", "Só existem no fundo do oceano"],
                "resposta": "São relativamente abundantes, mas raramente se encontram concentradas o suficiente para mineração rentável"
            },
            {
                "pergunta": "2. Qual destas aplicações é crucial para as 'Terras Raras' (ex: Neodímio)?",
                "opcoes": ["Fazer aço cirúrgico", "Produção de Ímanes Permanentes para turbinas eólicas e carros elétricos", "Tratamento de água do mar", "Alimentação de reatores nucleares"],
                "resposta": "Produção de Ímanes Permanentes para turbinas eólicas e carros elétricos"
            },
            {
                "pergunta": "3. Qual é o país que, historicamente, dominou a cadeia de fornecimento de Terras Raras nas últimas décadas?",
                "opcoes": ["Estados Unidos", "China", "Noruega", "Japão"],
                "resposta": "China"
            }
        ],
        "Silver": [
            {
                "pergunta": "1. Qual é a propriedade física suprema da Prata, superando todos os outros metais?",
                "opcoes": ["Maior dureza", "Maior densidade", "Maior condutividade elétrica e térmica", "Maior ponto de fusão"],
                "resposta": "Maior condutividade elétrica e térmica"
            },
            {
                "pergunta": "2. Além da joalharia e das moedas, qual é um uso industrial massivo da Prata hoje em dia?",
                "opcoes": ["Painéis solares (Células fotovoltaicas)", "Produção de asfalto", "Fuselagem de satélites", "Lâmpadas fluorescentes"],
                "resposta": "Painéis solares (Células fotovoltaicas)"
            },
            {
                "pergunta": "3. A grande maioria da Prata minerada não vem de minas puras de prata, mas sim como subproduto de...",
                "opcoes": ["Minas de carvão", "Extração de Chumbo, Zinco, Cobre e Ouro", "Minas de sal e calcário", "Extração de petróleo"],
                "resposta": "Extração de Chumbo, Zinco, Cobre e Ouro"
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
