import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    # Caminho dinâmico para evitar erros de localização
    base_path = os.path.dirname(__file__)
    csv_path = os.path.join(base_path, "..", "geology_dataset_standard.csv")
    
    df = pd.read_csv(csv_path)
    # Limpa espaços em branco nos nomes das colunas
    df.columns = df.columns.str.strip()
    return df

def get_mineral_names():
    df = load_data()
    # Retorna a lista de minerais únicos da coluna 'Resource'
    return sorted(df['Resource'].dropna().unique().tolist())

def get_mineral(mineral_resource):
    df = load_data()
    # Filtra pelo nome do recurso (ex: 'Sulfates')
    result = df[df['Resource'] == mineral_resource]
    if not result.empty:
        # Retornamos a primeira linha encontrada como dicionário
        return result.iloc[0].to_dict()
    return None

def get_top_occurrences(mineral_resource, limit=10):
    df = load_data()
    # Filtra todas as linhas para este mineral para mostrar no mapa
    occurrences = df[df['Resource'] == mineral_resource]
    return occurrences.head(limit).to_dict('records')

def mineral_exists(name):
    return name in get_mineral_names()