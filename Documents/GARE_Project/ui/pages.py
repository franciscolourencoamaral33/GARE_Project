import streamlit as st
import math
from core.data import get_mineral, get_mineral_names, get_top_occurrences
from services.map import build_folium_map
from streamlit_folium import st_folium

def render_home():
    # --- 1. O NOVO BANNER NA HOME ---
    try:
        st.image("images/home_banner.jpg", use_container_width=True)
    except:
        pass # Se não encontrar a imagem, não mostra erro, segue em frente
        
    st.markdown("<br>", unsafe_allow_html=True) # Espaçamento para respirar

    # --- 2. TÍTULO E INTRODUÇÃO ---
    st.title("Material ID - Geology Explorer")
    st.markdown("""
        Esta aplicação permite explorar e visualizar dados sobre os minerais vitais para a transição energética global.
        
        **Como usar:**
        1. Usa os botões abaixo ou a barra lateral para escolher um recurso.
        2. Navega pelas abas na barra lateral para ver Propriedades Físicas, Mapas e Geologia.
        3. Testa os teus conhecimentos no Quiz!
        
        ---
    """)
    
    st.subheader("Select a mineral resource to explore:")

    # --- 3. A TUA LÓGICA ORIGINAL DE BOTÕES ---
    names = get_mineral_names()

    if not names:
        st.warning("No minerals found in the database. Check your CSV file.")
        return

    cols = st.columns(3)
    for i, name in enumerate(names):
        with cols[i % 3]:
            # Se o botão for clicado:
            if st.button(name, key=f"btn_{name}", use_container_width=True):
                st.session_state['selected_mineral'] = name
                st.session_state['menu_option'] = "physical"
                st.rerun()
                
def render_physical(data):
    # 1. Vai buscar o nome usando a coluna exata que tens: 'resource'
    # Usamos .get() para que não dê erro se a coluna estiver vazia
    recurso_nome = data.get('resource', 'Unknown Resource')
    
    st.title(f"Details for {recurso_nome}")
    
    # 2. Truque da imagem (tira espaços e parênteses)
    mineral_filename = recurso_nome.lower().replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
    
    col_img, col_data = st.columns([1, 2])

    with col_img:
        image_path = f"images/{mineral_filename}.jpg"
        try:
            st.image(image_path, caption=recurso_nome, use_container_width=True)
        except:
            # Tenta carregar .jpeg caso a extensão seja essa
            try:
                st.image(f"images/{mineral_filename}.jpeg", caption=recurso_nome, use_container_width=True)
            except:
                st.warning(f"📷 Imagem não encontrada. Esperava-se '{mineral_filename}.jpg' na pasta 'images/'.")

    with col_data:
        # 3. Mostrar os dados que REALMENTE existem no teu ficheiro CSV
        st.markdown(f"**Specific Deposit/Name:** {data.get('name', 'N/A')}")
        st.write("---")
        
        st.write(f"""
        | Characteristic | Information |
        | :--- | :--- |
        | **Country** | {data.get('country', 'N/A')} |
        | **Geological Setting** | {data.get('geological setting', 'N/A')} |
        | **Host Rock** | {data.get('host rock', 'N/A')} |
        | **Deposit Type** | {data.get('deposit type', 'N/A')} |
        | **Status** | {data.get('status', 'N/A')} |
        """)

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

    # 2. Base de dados de perguntas (3 por mineral/recurso)
    questions_db = {
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
        "Lithium": [
            {
                "pergunta": "1. Qual é a principal aplicação deste recurso hoje em dia?",
                "opcoes": ["Construção Civil", "Baterias de iões de lítio", "Joalharia", "Combustível para aviões"],
                "resposta": "Baterias de iões de lítio"
            },
            {
                "pergunta": "2. Em que tipo de formação geológica é frequentemente extraído (ex: em Portugal ou Austrália)?",
                "opcoes": ["Pegmatitos", "Basalto", "Calcário", "Areia da praia"],
                "resposta": "Pegmatitos"
            },
            {
                "pergunta": "3. Qual destas características torna o Lítio único?",
                "opcoes": ["É magnético", "Brilha no escuro", "É o metal mais leve que existe", "É líquido à temperatura ambiente"],
                "resposta": "É o metal mais leve que existe"
            }
        ],
        "Methane Hydrate": [
            {
                "pergunta": "1. O que são os Hidratos de Metano (Methane Hydrates)?",
                "opcoes": ["Rochas vulcânicas ricas em gás", "Gelo inflamável que retém gás metano na sua estrutura", "Lagos subterrâneos de metano líquido", "Fósseis de dinossauros"],
                "resposta": "Gelo inflamável que retém gás metano na sua estrutura"
            },
            {
                "pergunta": "2. Onde se encontram tipicamente estas acumulações?",
                "opcoes": ["Nos desertos", "No topo de montanhas", "No fundo dos oceanos e no permafrost", "Em minas de sal"],
                "resposta": "No fundo dos oceanos e no permafrost"
            },
            {
                "pergunta": "3. Porque são considerados uma faca de dois gumes para o ambiente?",
                "opcoes": ["São altamente radioativos", "Consomem todo o oxigénio da água", "Podem libertar grandes quantidades de um potente gás de efeito estufa se derreterem", "Destroem a camada de ozono diretamente"],
                "resposta": "Podem libertar grandes quantidades de um potente gás de efeito estufa se derreterem"
            }
        ],
        "Monazite": [
            {
                "pergunta": "1. A Monazite é um mineral crucial para a extração de que grupo de elementos?",
                "opcoes": ["Ouro e Prata", "Terras Raras (REE) e Tório", "Ferro e Níquel", "Diamantes industriais"],
                "resposta": "Terras Raras (REE) e Tório"
            },
            {
                "pergunta": "2. Como é que a Monazite é frequentemente encontrada e extraída comercialmente?",
                "opcoes": ["Em areias pesadas costeiras (placers)", "Em minas profundas de carvão", "No núcleo de vulcões ativos", "Flutuando no oceano"],
                "resposta": "Em areias pesadas costeiras (placers)"
            },
            {
                "pergunta": "3. Devido à presença de urânio e tório, que cuidado especial exige este mineral?",
                "opcoes": ["Tem de ser guardado no escuro", "É frequentemente radioativo", "Muda de cor com a humidade", "Derrete ao sol"],
                "resposta": "É frequentemente radioativo"
            }
        ],
        "Orthoclase (K-feldspar)": [
            {
                "pergunta": "1. A Ortoclase é um mineral padrão na Escala de Mohs. Qual é a sua dureza?",
                "opcoes": ["1 (Muito mole)", "6", "10 (Dureza do diamante)", "8"],
                "resposta": "6"
            },
            {
                "pergunta": "2. É um mineral muito abundante. Em que tipo de rocha é um constituinte principal?",
                "opcoes": ["Granito", "Arenito", "Carvão", "Sal-gema"],
                "resposta": "Granito"
            },
            {
                "pergunta": "3. Qual é a principal aplicação industrial deste feldspato?",
                "opcoes": ["Combustível", "Alimentação animal", "Produção de vidro e cerâmica", "Construção de microchips"],
                "resposta": "Produção de vidro e cerâmica"
            }
        ],
        "Petroleum": [
            {
                "pergunta": "1. Como se formou a grande maioria do Petróleo que extraímos hoje?",
                "opcoes": ["A partir de dinossauros decompostos", "A partir de plâncton e algas marinhas pré-históricas sob calor e pressão", "A partir do magma terrestre", "Foi trazido por meteoritos"],
                "resposta": "A partir de plâncton e algas marinhas pré-históricas sob calor e pressão"
            },
            {
                "pergunta": "2. Qual é o principal tipo de rocha que serve de 'reservatório' para o petróleo?",
                "opcoes": ["Rochas sedimentares porosas (ex: arenitos e calcários)", "Granito maciço", "Mármore", "Obsidiana"],
                "resposta": "Rochas sedimentares porosas (ex: arenitos e calcários)"
            },
            {
                "pergunta": "3. Quimicamente, o petróleo é essencialmente uma mistura complexa de...",
                "opcoes": ["Hidratos de carbono", "Hidrocarbonetos", "Ácidos sulfúricos", "Gases nobres"],
                "resposta": "Hidrocarbonetos"
            }
        ],
        "Quartz": [
            {
                "pergunta": "1. Qual é a composição química simples do Quartzo?",
                "opcoes": ["Dióxido de Carbono (CO2)", "Dióxido de Silício (SiO2)", "Cloreto de Sódio (NaCl)", "Óxido de Ferro (Fe2O3)"],
                "resposta": "Dióxido de Silício (SiO2)"
            },
            {
                "pergunta": "2. Qual propriedade especial do Quartzo o torna útil em relógios e eletrónica?",
                "opcoes": ["Magnetismo", "Fluorescência", "Piezoeletricidade", "Condutividade térmica extrema"],
                "resposta": "Piezoeletricidade"
            },
            {
                "pergunta": "3. Qual é a dureza do Quartzo na Escala de Mohs?",
                "opcoes": ["5", "7", "9", "10"],
                "resposta": "7"
            }
        ],
        "Quartz (HPQ)": [
            {
                "pergunta": "1. O que significa a sigla HPQ associada a este quartzo?",
                "opcoes": ["High Pressure Quartz", "High Purity Quartz (Quartzo de Alta Pureza)", "Heavy Particle Quartz", "Hydro-Powered Quartz"],
                "resposta": "High Purity Quartz (Quartzo de Alta Pureza)"
            },
            {
                "pergunta": "2. Qual é a indústria moderna que depende criticamente do HPQ para os seus processos de fabrico?",
                "opcoes": ["Joalharia barata", "Indústria de Cimento", "Semicondutores e painéis solares", "Indústria Têxtil"],
                "resposta": "Semicondutores e painéis solares"
            },
            {
                "pergunta": "3. O que distingue o HPQ do quartzo comum encontrado em qualquer praia?",
                "opcoes": ["A sua cor totalmente negra", "Níveis extremamente baixos de impurezas", "A capacidade de flutuar", "É feito em laboratório"],
                "resposta": "Níveis extremamente baixos de impurezas"
            }
        ],
        "Sulfates": [
            {
                "pergunta": "1. Qual é o mineral de sulfato mais comum e amplamente utilizado na construção (ex: pladur/gesso cartonado)?",
                "opcoes": ["Pirite", "Gesso", "Bauxite", "Talco"],
                "resposta": "Gesso"
            },
            {
                "pergunta": "2. Em que tipo de ambiente geológico se formam muitos dos minerais de sulfato?",
                "opcoes": ["No núcleo terrestre", "Em ambientes de intensa evaporação (bacias evaporíticas)", "Em vulcões subaquáticos", "Em grutas glaciares"],
                "resposta": "Em ambientes de intensa evaporação (bacias evaporíticas)"
            },
            {
                "pergunta": "3. Quimicamente, todos os sulfatos contêm qual destes aniões?",
                "opcoes": ["Cloreto (Cl-)", "Carbonato (CO3 2-)", "Sulfato (SO4 2-)", "Nitrato (NO3-)"],
                "resposta": "Sulfato (SO4 2-)"
            }
        ],
        "Thorium": [
            {
                "pergunta": "1. Qual é o principal interesse do Tório para a tecnologia moderna?",
                "opcoes": ["Fazer aço inoxidável", "Combustível alternativo e mais seguro para reatores nucleares", "Baterias de telemóvel", "Isolamento acústico"],
                "resposta": "Combustível alternativo e mais seguro para reatores nucleares"
            },
            {
                "pergunta": "2. Comparativamente ao Urânio, quão abundante é o Tório na crosta terrestre?",
                "opcoes": ["É cerca de 3 a 4 vezes mais abundante", "São igualmente abundantes", "É muito mais raro", "Não existe naturalmente, só em meteoritos"],
                "resposta": "É cerca de 3 a 4 vezes mais abundante"
            },
            {
                "pergunta": "3. Em que mineral comum de areias pesadas se encontra muito do Tório mundial?",
                "opcoes": ["Quartzo", "Magnetite", "Monazite", "Mica"],
                "resposta": "Monazite"
            }
        ],
        "Uranium": [
            {
                "pergunta": "1. Qual é o principal minério de onde se extrai o Urânio?",
                "opcoes": ["Uraninite (Pechblenda)", "Galena", "Bauxite", "Cinábrio"],
                "resposta": "Uraninite (Pechblenda)"
            },
            {
                "pergunta": "2. Qual destes isótopos do Urânio é físsil e crucial para reatores nucleares de fissão?",
                "opcoes": ["Urânio-238", "Urânio-235", "Urânio-234", "Urânio-239"],
                "resposta": "Urânio-235"
            },
            {
                "pergunta": "3. Qual é o aspeto clássico do mineral Uraninite no seu estado natural (antes de ser refinado)?",
                "opcoes": ["Cristais verdes brilhantes", "Pedra preta ou acastanhada, densa e sem brilho metálico", "Pó amarelo brilhante ('yellowcake')", "Metal prateado e polido"],
                "resposta": "Pedra preta ou acastanhada, densa e sem brilho metálico"
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
        st.info(f"🚧 O quiz para **{mineral_name}** ainda não está disponível! Tenta outro recurso.")
        return

    # Criamos um "prefixo" para as chaves serem ÚNICAS para cada mineral
    prefix = mineral_name.replace(" ", "_").replace("(", "").replace(")", "")
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

    # 6. Avaliação Final
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
