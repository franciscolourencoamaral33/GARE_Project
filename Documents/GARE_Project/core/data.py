import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    # AQUI ESTÁ A CORREÇÃO DO NOME:
    csv_path = os.path.join(base_path, "..", "geo_dataset5_merged.csv")
    
    try:
        # sep=None e engine='python' resolvem o erro de "Expected 1 fields, saw 16"
        df = pd.read_csv(
            csv_path, 
            sep=None, 
            engine='python', 
            encoding='utf-8-sig',
            quotechar='"'
        )
        
        df.columns = df.columns.str.strip()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        if 'Latitude' in df.columns:
            df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        if 'Longitude' in df.columns:
            df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
            
        return df
    except Exception as e:
        st.error(f"Erro ao ler o CSV: {e}")
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
