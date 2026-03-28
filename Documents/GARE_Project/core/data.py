import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    csv_path = os.path.join(base_path, "..", "geology_dataset_standard.csv")
    
    try:
        # Tentativa 1: Leitura flexível com deteção automática
        df = pd.read_csv(csv_path, sep=None, engine='python', encoding='utf-8-sig')
        
        # Se o dataframe vier quase vazio, tentamos com ponto e vírgula (comum no Excel PT)
        if df.shape[1] <= 1:
            df = pd.read_csv(csv_path, sep=';', encoding='utf-8-sig')

        # Limpeza intensiva
        df.columns = df.columns.str.strip()
        # Remove linhas que sejam totalmente vazias
        df = df.dropna(how='all')
        
        # Limpa espaços em branco em todas as células de texto
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].astype(str).str.strip()
        
        return df
    except Exception as e:
        st.error(f"Erro ao ler o CSV: {e}")
        return pd.DataFrame()

def get_mineral_names():
    df = load_data()
    if df.empty:
        return []
    
    # Procura a coluna 'Resource' independentemente de maiúsculas/minúsculas
    col_map = {c.lower(): c for c in df.columns}
    target_col = col_map.get('resource', 'Resource')
    
    if target_col in df.columns:
        # Pega valores únicos, ignora 'nan' e ordena
        names = df[target_col].unique().tolist()
        names = [n for n in names if str(n).lower() != 'nan' and str(n) != ""]
        return sorted(names)
    return []

def get_mineral(mineral_resource):
    df = load_data()
    if df.empty: return None
    # Procura o primeiro que coincida
    result = df[df['Resource'] == mineral_resource]
    return result.iloc[0].to_dict() if not result.empty else None

def get_top_occurrences(mineral_resource, limit=10):
    df = load_data()
    if df.empty: return []
    occurrences = df[df['Resource'] == mineral_resource]
    return occurrences.head(limit).to_dict('records')

def mineral_exists(name):
    return name in get_mineral_names()