import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão Omega & Raphson", layout="wide")

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #2b468b; }
    [data-testid="stSidebar"] .st-expanderHeader, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h3 { color: white !important; }
    .main-title { color: #2b468b; font-size: 32px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAMENTO DA LOGO (VERSÃO REFORÇADA) ---
try:
    # Tenta carregar a imagem que está na mesma pasta do GitHub
    image = Image.open("logo_empresas.png")
    st.sidebar.image(image, use_container_width=True)
except Exception as e:
    # Se der erro, ele coloca um título bonito em vez do ícone quebrado
    st.sidebar.markdown("<h2 style='color:white; text-align:center;'>OMEGA & RAPHSON</h2>", unsafe_allow_html=True)

# --- MENU DE NAVEGAÇÃO ---
st.sidebar.divider()
modulo = st.sidebar.selectbox(
    "Escolha o Setor:", 
    ["Início", "🛠️ Manutenção", "🤝 Comercial", "💰 Financeiro", "📣 Marketing", "🛒 Compras", "⚙️ Configurações"]
)

# Título na tela principal
st.markdown("<div class='main-title'>Omega Inc & Raphson Engenharia</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Sistema Unificado de Gestão e Escalas</p>", unsafe_allow_html=True)
st.divider()

# --- LÓGICA DE DADOS (BANCO TEMPORÁRIO EM CSV) ---
def gerenciar_dados(nome):
    arquivo = f"dados_{nome}.csv"
    if os.path.exists(arquivo):
        return pd.read_csv(arquivo)
    return pd.DataFrame(columns=['ID', 'Data', 'Stand', 'Tarefa', 'Responsável', 'Escala', 'Status'])

# --- MÓDULO INÍCIO ---
if modulo == "Início":
    st.subheader("📍 Painel de Controle")
    col1, col2, col3 = st.columns(3)
    col1.metric("Projetos Ativos", "3", "Jazz, Live, Principal")
    col2.metric("Equipe em Campo", "8", "Técnicos")
    col3.metric("Status Global", "Operacional")
    st.info("Utilize o menu à esquerda para gerenciar os setores.")

# --- MÓDULOS DE GESTÃO ---
elif modulo in ["🛠️ Manutenção", "🤝 Comercial", "💰 Financeiro", "📣 Marketing", "🛒 Compras"]:
    setor_nome = modulo.split(" ")[1]
    st.subheader(f"Gestão de Escala - {setor_nome}")
    df = gerenciar_dados(setor_nome)
    
    with st.expander("➕ Nova Atribuição"):
        with st.form(f"form_{setor_nome}"):
            c1, c2 = st.columns(2)
            stand = c1.selectbox("Local:", ["Stand Jazz", "Stand Live", "Stand Principal", "Escritório"])
            resp = c2.text_input("Responsável:")
            escala = st.selectbox("Escala:", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"])
            tarefa = st.text_area("Descrição:")
            if st.form_submit_button("Registrar"):
                novo = pd.DataFrame([[len(df)+1, datetime.now().strftime("%d/%m/%Y"), stand, tarefa, resp, escala, "Pendente"]], columns=df.columns)
                df = pd.concat([df, novo], ignore_index=True)
                df.to_csv(f"dados_{setor_nome}.csv", index=False)
                st.success("Salvo com sucesso!")
                st.rerun()

    st.dataframe(df, use_container_width=True, hide_index=True)

elif modulo == "⚙️ Configurações":
    st.subheader("Configurações")
    st.write("Em breve: Integração direta com Google Sheets.")
