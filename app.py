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
                ),
                "ID": st.column_config.Column(disabled=True),
                "Stand": st.column_config.Column(disabled=True),
                "Descrição": st.column_config.Column(disabled=True),
                "Prioridade": st.column_config.Column(disabled=True)
            },
            hide_index=True, 
            use_container_width=True, 
            key="editor_backlog"
        )
        
        # Se você alterar o status na tabela, o sistema salva automaticamente
        if not df_editado.equals(st.session_state['chamados']):
            st.session_state['chamados'] = df_editado
            salvar_dados()

        # Botão Popover para Solicitação de Materiais
        with st.popover("Solicitar Material ao Setor de Compras 📦", use_container_width=True):
            st.markdown("#### Requisição de Ferramentas/Materiais")
            with st.form("f_material_req", clear_on_submit=True):
                ids_os = st.session_state['chamados']['ID'].tolist()
                os_sel = st.selectbox("Referência (OS)", ids_os if ids_os else ["Nenhuma OS aberta"])
                
                # Cálculo automático do próximo item
                num_item = len(st.session_state['solicitacoes_material']) + 1
                st.info(f"**Item:** {num_item}")
                
                mat_txt = st.text_input("Material/Ferramenta")
                qtd_num = st.number_input("Quantidade", min_value=1, step=1)
                
                if st.form_submit_button("Enviar Solicitação"):
                    st.session_state['solicitacoes_material'].append({
                        "Item": num_item, 
                        "OS": os_sel, 
                        "Material": mat_txt, 
                        "Qtd": qtd_num, 
                        "Data": str(datetime.date.today())
                    })
                    salvar_dados()
                    st.success("Item solicitado com sucesso!")

def module_cadastro():
    st.header("📝 Gestão de Cadastros")
    st.info("💡 **Dica de Exclusão:** Para excluir um registro, clique na caixinha à esquerda da linha que deseja apagar, pressione a tecla **Delete** no teclado e clique no botão de Salvar abaixo da tabela.")
    
    tab1, tab2, tab3 = st.tabs(["Usuários", "Stands de Vendas", "Centros de Custo"])
    
    with tab1:
        st.session_state['usuarios'] = st.data_editor(st.session_state['usuarios'], num_rows="dynamic", use_container_width=True, key="edit_u")
        if st.button("Salvar Alterações de Usuários", type="primary"):
            salvar_dados()
            st.success("Tabela de Usuários atualizada no banco de dados!")

    with tab2:
        st.session_state['stands'] = st.data_editor(st.session_state['stands'], num_rows="dynamic", use_container_width=True, key="edit_s")
        if st.button("Salvar Alterações de Stands", type="primary"):
            salvar_dados()
            st.success("Tabela de Stands atualizada no banco de dados!")
            
    with tab3:
        st.session_state['centros_custo'] = st.data_editor(st.session_state['centros_custo'], num_rows="dynamic", use_container_width=True, key="edit_c")
        if st.button("Salvar Alterações de Centros de Custo", type="primary"):
            salvar_dados()
            st.success("Tabela de Centros de Custo atualizada no banco de dados!")

def module_painel_gestao():
    st.header("📊 Painel de Gestão")
    st.write("Bem-vindo ao centro de controle operacional.")

# --- FLUXO PRINCIPAL ---
def main():
    if not st.session_state['autenticado']:
        col1, col2, col3 = st.columns([1.5, 1, 1.5])
        with col2:
            st.markdown("<h3 style='text-align: center;'>Acesso Restrito</h3>", unsafe_allow_html=True)
            u = st.text_input("E-mail")
            p = st.text_input("Senha", type="password")
            if st.button("Entrar", use_container_width=True):
                if p == "1234": # Simulação de senha rápida para seus testes
                    st.session_state['autenticado'] = True
                    st.rerun()
                else:
                    st.error("Credenciais incorretas.")
    else:
        with st.sidebar:
            exibir_logo_sidebar()
            st.divider()
            
            # Botões de Navegação do Menu
            modulos = ["Painel de Gestão", "Manutenção", "Cadastro"]
            for mod in modulos:
                if st.button(mod, use_container_width=True, type="primary" if st.session_state['pagina_atual'] == mod else "secondary"):
                    st.session_state['pagina_atual'] = mod
                    st.rerun()
            
            st.divider()
            st.caption(f"Logado como: Raphael")
            
            if st.button("Sair", use_container_width=True):
                st.session_state['autenticado'] = False
                st.rerun()

        # Renderizador de Páginas
        pag = st.session_state['pagina_atual']
        if pag == "Manutenção": module_manutencao()
        elif pag == "Cadastro": module_cadastro()
        elif pag == "Painel de Gestão": module_painel_gestao()

if __name__ == "__main__":
    main()
