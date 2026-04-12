import streamlit as st
import pandas as pd
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão Omega & Raphson", layout="wide", page_icon="🏗️")

# --- 1. CONFIGURAÇÃO DO LINK DA PLANILHA ---
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1GjNaksY3_N2AxVvMdVtr2L-0Zk2DXT3luZUwbdNFpeA/edit?gid=0#gid=0"

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

# --- 3. PÁGINA INICIAL (DASHBOARD DE GESTÃO) ---
if modulo == "🏠 Início":
    st.title("Painel de Gestão Integrada")
    st.subheader("Visão Geral da Operação")
    
    # Criando os Cards de Métricas (Dashboard)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Stands Ativos", value="3", delta="Jazz, Live, Principal")
    
    with col2:
        st.metric(label="Status da Operação", value="Normal", delta="0 Alertas")
        
    with col3:
        st.metric(label="Manutenções Pendentes", value="Ver Planilha", delta_color="off")

    st.divider()
    
    st.markdown("### Informativos Recentes")
    st.info("Utilize o menu lateral para registrar manutenções ou visualizar relatórios detalhados.")

# --- 4. MÓDULO DE MANUTENÇÃO ---
elif modulo == "🛠️ Manutenção":
    st.subheader("Registro de Atividades de Manutenção")
    if CSV_URL:
        try:
            df = pd.read_csv(CSV_URL)
            st.write("### Visualização de Dados")
            st.dataframe(df, use_container_width=True)
        except:
            st.error("Erro ao carregar os dados. Verifique a publicação da planilha.")
    else:
        st.warning("Configuração de banco de dados pendente.")

# --- 5. RELATÓRIOS ---
elif modulo == "📊 Relatórios":
    st.subheader("Análise de Produtividade")
    st.info("Os gráficos de desempenho serão gerados automaticamente conforme o preenchimento da planilha.")
