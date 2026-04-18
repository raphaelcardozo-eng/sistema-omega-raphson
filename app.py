import streamlit as st
import pandas as pd
from PIL import Image
import datetime
import json
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Omega & Raphson ERP", layout="wide")

# --- SISTEMA DE PERSISTÊNCIA ---
DB_FILE = "database_erp.json"

def salvar_dados():
    # Converte dataframes para dicionários para salvar em JSON
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

# --- INICIALIZAÇÃO DE ESTADO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
    st.session_state['pagina_atual'] = "Painel de Gestão"
    
    # Tenta carregar dados salvos. Se não existir, cria estrutura básica.
    if not carregar_dados():
        st.session_state['usuarios'] = pd.DataFrame([{"Nome": "Raphael Cardozo", "Email": "raphaelcardozo@raphsonengenharia.com.br", "Perfil": "Diretor", "Senha": "1234", "Status": "Ativo"}])
        st.session_state['stands'] = pd.DataFrame(columns=["Nome do Stand", "Endereço", "Status"])
        st.session_state['centros_custo'] = pd.DataFrame(columns=["Nome do Centro de Custo", "CNPJ", "Status"])
        st.session_state['chamados'] = pd.DataFrame(columns=["ID", "Stand", "Descrição", "Status", "Prioridade"])
        st.session_state['solicitacoes_material'] = []

# --- FUNÇÃO DE LOGO (CORRIGIDA) ---
def exibir_logo_sidebar():
    try:
        # Tenta carregar a imagem local
        img = Image.open("Image_from_Image.jpg")
        st.sidebar.image(img, use_container_width=True)
    except:
        # Se falhar, exibe apenas o nome em texto para não quebrar o menu
        st.sidebar.subheader("Omega & Raphson")

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
                new_id = f"OS-{len(st.session_state['chamados']) + 1:03d}"
                nova_os = pd.DataFrame([{"ID": new_id, "Stand": stand, "Descrição": desc, "Status": "Aguardando atendimento", "Prioridade": prio}])
                st.session_state['chamados'] = pd.concat([st.session_state['chamados'], nova_os], ignore_index=True)
                salvar_dados()
                st.rerun()
                    
    with col_b:
        st.subheader("Backlog de Manutenção")
        # Tabela com bloqueio de edição exceto Status
        edited_df = st.data_editor(
            st.session_state['chamados'],
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status", 
                    options=["Aguardando atendimento", "Em andamento", "Aguardando Material", "Concluído", "Cancelada"],
                    required=True
                ),
                "ID": st.column_config.Column(disabled=True),
                "Stand": st.column_config.Column(disabled=True),
                "Descrição": st.column_config.Column(disabled=True),
                "Prioridade": st.column_config.Column(disabled=True)
            },
            hide_index=True, use_container_width=True, key="editor_backlog"
        )
        
        # Salva se houver alteração no status
        if not edited_df.equals(st.session_state['chamados']):
            st.session_state['chamados'] = edited_df
            salvar_dados()

        # Botão solicitar material
        with st.popover("Solicitar Material ao Setor de Compras 📦", use_container_width=True):
            with st.form("f_material_req", clear_on_submit=True):
                ids_os = st.session_state['chamados']['ID'].tolist()
                os_sel = st.selectbox("Selecione a OS", ids_os if ids_os else ["Sem OS"])
                num_item = len(st.session_state['solicitacoes_material']) + 1
                st.write(f"**Item:** {num_item}")
                mat_txt = st.text_input("Material/Ferramenta")
                qtd_num = st.number_input("Quantidade", min_value=1)
                
                if st.form_submit_button("Enviar Solicitação"):
                    st.session_state['solicitacoes_material'].append({
                        "Item": num_item, "OS": os_sel, "Material": mat_txt, "Qtd": qtd_num, "Data": str(datetime.date.today())
                    })
                    salvar_dados()
                    st.success("Solicitação salva!")

def module_cadastro():
    st.header("📝 Gestão de Cadastros")
    tab1, tab2, tab3 = st.tabs(["Usuários", "Stands", "Centros de Custo"])
    
    with tab1:
        st.write("Dica: Use a tecla 'Delete' para excluir e clique em Salvar.")
        st.session_state['usuarios'] = st.data_editor(st.session_state['usuarios'], num_rows="dynamic", use_container_width=True, key="edit_u")
        if st.button("Salvar Alterações de Usuários"):
            salvar_dados()
            st.success("Usuários atualizados!")

    with tab2:
        st.session_state['stands'] = st.data_editor(st.session_state['stands'], num_rows="dynamic", use_container_width=True, key="edit_s")
        if st.button("Salvar Alterações de Stands"):
            salvar_dados()
            st.success("Stands atualizados!")
            
    with tab3:
        st.session_state['centros_custo'] = st.data_editor(st.session_state['centros_custo'], num_rows="dynamic", use_container_width=True, key="edit_c")
        if st.button("Salvar Alterações de CC"):
            salvar_dados()
            st.success("Centros de Custo atualizados!")

# --- ESTRUTURA PRINCIPAL ---
def main():
    if not st.session_state['autenticado']:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.title("Login")
            u = st.text_input("E-mail")
            p = st.text_input("Senha", type="password")
            if st.button("Entrar", use_container_width=True):
                if p == "1234": # Simulação de senha rápida para seu teste
                    st.session_state['autenticado'] = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
    else:
        # MENU LATERAL CORRIGIDO
        with st.sidebar:
            exibir_logo_sidebar()
            st.divider()
            st.markdown("### Navegação")
            
            # Botões de navegação
            if st.button("📊 Painel de Gestão", use_container_width=True): st.session_state['pagina_atual'] = "Painel de Gestão"
            if st.button("🔧 Manutenção", use_container_width=True): st.session_state['pagina_atual'] = "Manutenção"
            if st.button("📝 Cadastros", use_container_width=True): st.session_state['pagina_atual'] = "Cadastro"
            
            st.sidebar.write(f"Usuário: {st.session_state.get('usuario_logado', 'Raphael')}")
            
            if st.button("Sair", type="secondary"):
                st.session_state['autenticado'] = False
                st.rerun()

        # RENDERIZAÇÃO DA PÁGINA ATUAL
        p = st.session_state['pagina_atual']
        if p == "Manutenção": module_manutencao()
        elif p == "Cadastro": module_cadastro()
        else:
            st.title("📊 Painel de Gestão")
            st.write("Bem-vindo ao centro de controle operacional.")

if __name__ == "__main__":
    main()
