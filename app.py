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
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            dados = json.load(f)
            st.session_state['usuarios'] = pd.DataFrame(dados["usuarios"])
            st.session_state['stands'] = pd.DataFrame(dados["stands"])
            st.session_state['centros_custo'] = pd.DataFrame(dados["centros"])
            st.session_state['chamados'] = pd.DataFrame(dados["chamados"])
            st.session_state['solicitacoes_material'] = dados["materiais"]
            return True
    return False

# --- INICIALIZAÇÃO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
    st.session_state['pagina_atual'] = "Painel de Gestão"
    
    # Tenta carregar do arquivo, se falhar, cria vazio
    if not carregar_dados():
        st.session_state['usuarios'] = pd.DataFrame([{"Nome": "Raphael Cardozo", "Email": "raphaelcardozo@raphsonengenharia.com.br", "Perfil": "Diretor", "Senha": "1234", "Status": "Ativo"}])
        st.session_state['stands'] = pd.DataFrame(columns=["Nome do Stand", "Endereço", "Status"])
        st.session_state['centros_custo'] = pd.DataFrame(columns=["Nome do Centro de Custo", "CNPJ", "Status"])
        st.session_state['chamados'] = pd.DataFrame(columns=["ID", "Stand", "Descrição", "Status", "Prioridade"])
        st.session_state['solicitacoes_material'] = []

def carregar_logo():
    try: return Image.open("Image_from_Image.jpg")
    except: return None

# --- MÓDULOS ---

def module_manutencao():
    st.header("🔧 Manutenção")
    col_f, col_b = st.columns([1, 2])
    
    with col_f:
        st.subheader("Abertura de Chamado")
        with st.form("form_os", clear_on_submit=True):
            lista_s = st.session_state['stands']['Nome do Stand'].tolist()
            stand = st.selectbox("Stand", lista_s if lista_s else ["Nenhum"])
            desc = st.text_area("Descrição")
            prio = st.selectbox("Prioridade", ["Baixa", "Média", "Alta", "Urgente"])
            if st.form_submit_button("Abrir OS"):
                new_id = f"OS-{len(st.session_state['chamados']) + 1:03d}"
                nova_os = pd.DataFrame([{"ID": new_id, "Stand": stand, "Descrição": desc, "Status": "Aguardando atendimento", "Prioridade": prio}])
                st.session_state['chamados'] = pd.concat([st.session_state['chamados'], nova_os], ignore_index=True)
                salvar_dados() # SALVA NO ARQUIVO
                st.rerun()
                    
    with col_b:
        st.subheader("Backlog de Manutenção")
        # Backlog com Status editável e campos protegidos
        chamados_editados = st.data_editor(
            st.session_state['chamados'],
            column_config={
                "Status": st.column_config.SelectboxColumn("Status", options=["Aguardando atendimento", "Em andamento", "Aguardando Material", "Concluído", "Cancelada"]),
                "ID": st.column_config.Column(disabled=True),
                "Stand": st.column_config.Column(disabled=True),
                "Descrição": st.column_config.Column(disabled=True)
            },
            hide_index=True, use_container_width=True, key="backlog_editor"
        )
        
        # Se houver mudança no status, salva
        if not chamados_editados.equals(st.session_state['chamados']):
            st.session_state['chamados'] = chamados_editados
            salvar_dados()

        # POP OVER PARA MATERIAIS
        with st.popover("Solicitar Material 📦", use_container_width=True):
            with st.form("f_mat", clear_on_submit=True):
                ids = st.session_state['chamados']['ID'].tolist()
                os_ref = st.selectbox("OS", ids if ids else ["-"])
                proximo = len(st.session_state['solicitacoes_material']) + 1
                mat = st.text_input(f"Item {proximo} - Material")
                qtd = st.number_input("Qtd", min_value=1)
                if st.form_submit_button("Confirmar"):
                    st.session_state['solicitacoes_material'].append({"Item": proximo, "OS": os_ref, "Material": mat, "Qtd": qtd})
                    salvar_dados()
                    st.success("Salvo!")

def module_cadastro():
    st.header("📝 Gestão de Registros")
    tab1, tab2 = st.tabs(["Usuários", "Stands"])
    
    with tab1:
        st.session_state['usuarios'] = st.data_editor(st.session_state['usuarios'], num_rows="dynamic", use_container_width=True, key="ed_user")
        if st.button("Confirmar Alterações/Exclusões de Usuários"):
            salvar_dados()
            st.success("Banco de dados atualizado!")

    with tab2:
        st.session_state['stands'] = st.data_editor(st.session_state['stands'], num_rows="dynamic", use_container_width=True, key="ed_stand")
        if st.button("Confirmar Alterações/Exclusões de Stands"):
            salvar_dados()
            st.rerun()

# --- ESTRUTURA PRINCIPAL ---
def main():
    if not st.session_state['autenticado']:
        # Login (Reduzido como solicitado anteriormente)
        col1, col2, col3 = st.columns([1.5, 1, 1.5])
        with col2:
            logo = carregar_logo()
            if logo: st.image(logo, use_container_width=True)
            user = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar", use_container_width=True):
                if senha == "1234": # Simplificado para teste
                    st.session_state['autenticado'] = True
                    st.rerun()
    else:
        with st.sidebar:
            st.image(carregar_logo(), use_container_width=True) if carregar_logo() else None
            if st.button("Painel de Gestão", use_container_width=True): st.session_state['pagina_atual'] = "Painel de Gestão"
            if st.button("Cadastro", use_container_width=True): st.session_state['pagina_atual'] = "Cadastro"
            if st.button("Manutenção", use_container_width=True): st.session_state['pagina_atual'] = "Manutenção"
            st.divider()
            if st.button("Sair"): 
                st.session_state['autenticado'] = False
                st.rerun()
        
        pag = st.session_state['pagina_atual']
        if pag == "Manutenção": module_manutencao()
        elif pag == "Cadastro": module_cadastro()
        else: st.title(pag)

if __name__ == "__main__":
    main()
