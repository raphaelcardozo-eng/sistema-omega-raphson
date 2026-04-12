import streamlit as st
import pandas as pd
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão Omega & Raphson", layout="wide", page_icon="🏗️")

# --- 1. CONFIGURAÇÃO DO LINK DA PLANILHA ---
# COLE O LINK QUE VOCÊ COPIOU DO BOTÃO COMPARTILHAR ENTRE AS ASPAS ABAIXO:
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1GjNaksY3_N2AxVvMdVtr2L-0Zk2DXT3luZUwbdNFpeA/edit?gid=0#gid=0"

# Esta linha transforma o link normal em um link que o Python consegue ler (formato CSV)
if "docs.google.com" in URL_PLANILHA:
    CSV_URL = URL_PLANILHA.replace('/edit?usp=sharing', '/export?format=csv').replace('/edit', '/export?format=csv')
else:
    CSV_URL = None

# --- 2. LOGO E SIDEBAR ---
with st.sidebar:
    try:
        # Tenta carregar sua logo se o arquivo estiver no GitHub
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

# --- 4. MÓDULO DE MANUTENÇÃO (LEITURA DA PLANILHA) ---
elif modulo == "🛠️ Manutenção":
    st.subheader("Registro de Atividades de Manutenção")
    
    if CSV_URL:
        try:
            # Lendo os dados em tempo real
            df = pd.read_csv(CSV_URL)
            
            # Filtros rápidos
            st.write("### Filtros")
            col1, col2 = st.columns(2)
            with col1:
                filtro_stand = st.multiselect("Filtrar por Stand:", options=df.iloc[:, 0].unique())
            
            # Exibição da Tabela
            st.write("### Dados da Planilha")
            if filtro_stand:
                df_filtrado = df[df.iloc[:, 0].isin(filtro_stand)]
                st.dataframe(df_filtrado, use_container_width=True)
            else:
                st.dataframe(df, use_container_width=True)
                
            st.success("Dados atualizados em tempo real diretamente do Google Sheets.")
            
        except Exception as e:
            st.error("Erro ao ler a planilha. Verifique se você a 'Publicou na Web' e se o link está correto.")
            st.info("Passo para corrigir: Arquivo > Compartilhar > Publicar na Web.")
    else:
        st.warning("Por favor, insira o link da planilha no código `app.py` para visualizar os dados.")

# --- 5. RELATÓRIOS ---
elif modulo == "📊 Relatórios":
    st.subheader("Análise de Produtividade")
    st.write("Gráficos e indicadores serão exibidos aqui conforme os dados da planilha crescerem.")
