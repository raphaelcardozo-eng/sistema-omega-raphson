import streamlit as st
import pandas as pd
from PIL import Image
import datetime
import json
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Omega & Raphson ERP", layout="wide")

# --- SISTEMA DE PERSISTÊNCIA (SALVAR/CARREGAR) ---
DB_FILE = "database_erp.json"

def salvar_dados():
    # Converte os dataframes para dicionários para salvar no arquivo JSON
    dados = {
        "usuarios": st.session_state['usuarios'].to_dict(orient="records"),
        "stands": st.session_state['stands'].to_dict(orient="records"),
        "centros": st.session_state['centros_custo'].to_dict(orient="records"),
        "chamados": st.session_state['chamados'].to_dict(orient="records"),
        "materiais": st.session_state['solicitacoes_material']
    }
    with open(DB_FILE, "w") as f:
        json.dump(dados, f, default=str)

def carregar_dados():
    # Carrega os dados do JSON para a memória do sistema
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                dados = json.load(f)
                st.session_state['usuarios'] = pd.DataFrame(dados["usuarios"])
                st.session_state['stands'] = pd.DataFrame(dados["stands"])
                st.session_state['centros_custo'] = pd.DataFrame(dados["centros"])
                st.session_state['chamados'] = pd.DataFrame(dados["chamados"])
                st.session_state['solicitacoes_material'] = dados["materiais"]
                return True
        except:
            return False
    return False

# --- INICIALIZAÇÃO DE VARIÁVEIS DE SESSÃO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
    st.session_state['pagina_atual'] = "Painel de Gestão"
    
    # Se não conseguir carregar o arquivo, cria tabelas vazias/padrão
    if not carregar_dados():
        st.session_state['usuarios'] = pd.DataFrame([{"Nome": "Raphael Cardozo", "Email": "raphaelcardozo@raphsonengenharia.com.br", "Perfil": "Diretor", "Senha": "1234", "Status": "Ativo"}])
        st.session_state['stands'] = pd.DataFrame(columns=["Nome do Stand", "Endereço", "Prazo de Locação", "Status"])
        st.session_state['centros_custo'] = pd.DataFrame(columns=["Nome do Centro de Custo", "CNPJ", "Descrição", "Status"])
        st.session_state['chamados'] = pd.DataFrame(columns=["ID", "Stand", "Descrição", "Status", "Prioridade"])
        st.session_state['solicitacoes_material'] = []

# --- FUNÇÃO DE LOGO SEGURA ---
def exibir_logo_sidebar():
    try:
        img = Image.open("Image_from_Image.jpg")
        st.sidebar.image(img, use_container_width=True)
    except:
        st.sidebar.markdown("### Omega & Raphson")

# --- MÓDULOS ---

def module_manutencao():
    st.header("🔧 Manutenção")
    col_f, col_b = st.columns([1, 2])
    
    with col_f:
        st.subheader("Abertura de Chamado")
        with st.form("form_os", clear_on_submit=True):
            lista_s = st.session_state['stands']['Nome do Stand'].tolist()
            stand = st.selectbox("Stand", lista_s if lista_s else ["Nenhum Stand Cadastrado"])
            desc = st.text_area("Descrição do Problema")
            prio = st.selectbox("Prioridade", ["Baixa", "Média", "Alta", "Urgente"])
            
            if st.form_submit_button("Abrir OS"):
                if not lista_s:
                    st.error("Cadastre um Stand primeiro!")
                else:
                    new_id = f"OS-{len(st.session_state['chamados']) + 1:03d}"
                    nova_os = pd.DataFrame([{"ID": new_id, "Stand": stand, "Descrição": desc, "Status": "Aguardando atendimento", "Prioridade": prio}])
                    st.session_state['chamados'] = pd.concat([st.session_state['chamados'], nova_os], ignore_index=True)
                    salvar_dados()
                    st.rerun()
                    
    with col_b:
        st.subheader("Backlog de Manutenção")
        
        # Tabela Bloqueada: Apenas a coluna Status pode ser editada com opções pré-definidas
        df_editado = st.data_editor(
            st.session_state['chamados'],
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status", 
                    options=["Aguardando atendimento", "Em andamento", "Aguardando Material", "Concluído", "Cancelada"],
                    required=True
