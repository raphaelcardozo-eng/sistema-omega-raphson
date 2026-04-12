import streamlit as st
import pandas as pd
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão Omega & Raphson", layout="wide", page_icon="🏗️")

# --- 1. CONFIGURAÇÃO DO LINK DA PLANILHA ---
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1GjNaksY3_N2AxVvMdVtr2L-0Zk2DXT3luZUwbdNFpeA/edit?gid=0#gid=0"

# Limpeza do link para leitura em CSV
if "docs.google.com" in URL_PLANILHA:
    CSV_URL = URL_PLANILHA.split("/edit")[0] + "/export?format=csv"
else:
    CSV_URL = None

# --- 2. LOGO E SIDEBAR ---
with st.sidebar:
    try:
        image = Image.open("logo_empresas.png")
        st.image(image, use_container_width=True)
    except:
        st.title("🏢 OMEGA & RAPHSON")
    
    st.divider()
    modulo = st.selectbox("Escolha o Setor:", ["🏠 Início", "🛠️ Manutenção", "📊 Relatórios"])

# --- 3. PÁGINA INICIAL ---
if modulo == "🏠 Início":
    st.title("Painel de Controle Omega & Raphson")
    st.markdown(f"""
    ### Bem-vindo ao Sistema Unificado
    Este painel está conectado diretamente à sua Planilha Google.
    
    * **Status do Banco de Dados:** {"✅ Conectado" if CSV_URL else "❌ Link não configurado"}
    * **Equipe Ativa:** Jazz, Live, Principal.
    """)
    st.info("Utilize o menu lateral para navegar entre os setores.")

# --- 4. MÓDULO DE MANUTENÇÃO ---
elif modulo == "🛠️ Manutenção":
    st.subheader("Registro de Atividades de Manutenção")
    if CSV_URL:
        try:
            df = pd.read_csv(CSV_URL)
            st.write("### Dados da Planilha")
            st.dataframe(df, use_container_width=True)
            st.success("Dados atualizados em tempo real!")
        except Exception as e:
            st.error("Erro ao ler a planilha. Verifique se ela foi 'Publicada na Web'.")
    else:
        st.warning("Link da planilha não configurado corretamente.")

# --- 5. RELATÓRIOS ---
elif modulo == "📊 Relatórios":
    st.subheader("Análise de Produtividade")
    st.write("Em desenvolvimento.")
