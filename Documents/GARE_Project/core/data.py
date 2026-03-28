import pandas as pd
import streamlit as st
import os

@st.cache_data(ttl=1)
def load_data():
    base_path = os.path.dirname(__file__)
    csv_path = os.path.join(base_path, "..", "geology_dataset_standard.csv")
    
    try:
        # Definimos exatamente as colunas que queremos ler para evitar o erro de 'fields expected'
        cols_to_use = [
            'Dataset', 'Resource', 'Name', 'Country', 'Latitude', 'Longitude', 
            'Geological Setting', 'Host Rock / Reservoir', 'Deposit Type / Trap Type', 
            'Grade / Concentration', 'Size / Reserves', 'Depth', 'Temperature', 
            'Status', 'Notes', 'Source'
        ]
        
        # Leitura forçada com delimitador vírgula e ignorando erros de linha
        df = pd.read_csv(
            csv_path, 
            usecols=cols_to_use,
            encoding='utf-8-sig',
            on_bad_lines='skip',
            sep=','
        )
        
        # Limpeza de espaços
        df.columns = df.columns.str.strip()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        return df
    except Exception as e:
        # Se falhar com vírgula, tenta com ponto e vírgula
        try:
            df = pd.read_csv(csv_path, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
            return df
        except:
            st.error(f"Erro na leitura do CSV: {e}")
            return pd.DataFrame()

def get_mineral_names():
    df = load_data()
    if df.empty: return []
    if 'Resource' in df.columns:
        names = df['Resource'].unique().tolist()
        return sorted([str(n) for n in names if str(n).lower() != 'nan' and str(n).strip() != ""])
    return []

def get_mineral(mineral_resource):
    df = load_data()
    if df.empty: return None
    result = df[df['Resource'] == mineral_resource]
    return result.iloc[0].to_dict() if not result.empty else None

def get_top_occurrences(mineral_resource, limit=10):
    df = load_data()
    if df.empty: return []
    occurrences = df[df['Resource'] == mineral_resource]
    return occurrences.head(limit).to_dict('records')

def mineral_exists(name):
    return name in get_mineral_names()