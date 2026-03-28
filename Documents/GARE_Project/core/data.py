import pandas as pd
import streamlit as st
import os


@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    csv_path = os.path.join(base_path, "..", "geology_dataset_standard.csv")
    
    try:
        # Forçamos a leitura e removemos linhas totalmente vazias
        df = pd.read_csv(
            csv_path, 
            sep=None, 
            engine='python', 
            encoding='utf-8-sig', # O 'sig' ajuda com ficheiros do Excel/Numbers
            on_bad_lines='skip'
        )
        
        # REMOVE LINHAS DUPLICADAS E ESPAÇOS EM BRANCO NAS COLUNAS
        df.columns = df.columns.str.strip()
        
        # Limpa espaços em branco dentro de todas as células de texto do CSV
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        return df
    except Exception as e:
        st.error(f"Erro crítico no CSV: {e}")
        return pd.DataFrame()
    
def get_mineral_names():
    df = load_data()
    if df.empty:
        return []
    
    # Vamos garantir que ele lê a coluna 'Resource'
    if 'Resource' in df.columns:
        # Pega em tudo o que não é vazio e remove duplicados
        lista = df['Resource'].unique().tolist()
        # Filtra para não aparecerem valores como 'nan' ou vazios
        lista = [x for x in lista if str(x).lower() != 'nan' and str(x).strip() != ""]
        return sorted(lista)
    return []

def get_mineral(mineral_resource):
    df = load_data()
    if df.empty:
        return None
    # Filtra pelo nome do recurso
    result = df[df['Resource'] == mineral_resource]
    if not result.empty:
        return result.iloc[0].to_dict()
    return None

def get_top_occurrences(mineral_resource, limit=10):
    df = load_data()
    if df.empty:
        return []
    # Filtra ocorrências para o mapa
    occurrences = df[df['Resource'] == mineral_resource]
    return occurrences.head(limit).to_dict('records')

def mineral_exists(name):
    return name in get_mineral_names()