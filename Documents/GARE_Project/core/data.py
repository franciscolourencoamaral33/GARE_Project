import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    # Caminho dinâmico para localizar o CSV na pasta acima de 'core'
    base_path = os.path.dirname(__file__)
    csv_path = os.path.join(base_path, "..", "geology_dataset_standard.csv")
    
    try:
        # sep=None com engine='python' deteta automaticamente se o separador é , ou ;
        # on_bad_lines='skip' ignora linhas com erros de formatação
        df = pd.read_csv(
            csv_path, 
            sep=None, 
            engine='python', 
            on_bad_lines='skip', 
            encoding='utf-8'
        )
        
        # Remove espaços em branco extras nos nomes das colunas
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o ficheiro CSV: {e}")
        return pd.DataFrame()

def get_mineral_names():
    df = load_data()
    if df.empty:
        return []
    
    # Vamos garantir que o Pandas olha para a coluna certa, 
    # ignorando espaços extras que o Excel às vezes mete.
    column_name = 'Resource' 
    
    if column_name in df.columns:
        # Pega em todos os valores, remove espaços e valores vazios
        names = df[column_name].dropna().unique().tolist()
        # Limpa espaços em branco de cada nome (ex: "Quartz " vira "Quartz")
        names = [str(n).strip() for n in names]
        # Remove duplicados que possam ter surgido da limpeza e ordena
        return sorted(list(set(names)))
    else:
        st.warning(f"Colunas encontradas: {list(df.columns)}")
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