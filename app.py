import streamlit as st
import pandas as pd
from PIL import Image
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Omega & Raphson ERP", layout="wide", initial_sidebar_state="expanded")

# --- FUNÇÃO PARA CARREGAR LOGO ---
def carregar_logo():
    try:
        return Image.open("Image_from_Image.jpg")
    except FileNotFoundError:
        return None

# --- INICIALIZAÇÃO DE BANCO DE DADOS TEMPORÁRIO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'pagina_atual' not in st.session_state:
    st.session_state['pagina_atual'] = "Painel de Gestão"
if 'usuario_logado' not in st.session_state:
    st.session_state['usuario_logado'] = ""
if 'precisa_trocar_senha' not in st.session_state:
    st.session_state['precisa_trocar_senha'] = False

# Tabelas de Cadastro (Com novas colunas de Senha e CNPJ)
if 'usuarios' not in st.session_state:
    # Criamos um usuário admin padrão para você não perder o acesso
    dados_iniciais = [{
        "Nome": "Raphael Cardozo", 
        "Email": "raphaelcardozo@raphsonengenharia.com.br", 
        "Telefone": "", 
        "Perfil": "Diretor", 
        "Senha": "1234", 
        "Primeiro_Acesso": False, 
        "Data_Ultima_Senha": datetime.date.today(),
        "Status": "Ativo"
    }]
    st.session_state['usuarios'] = pd.DataFrame(dados_iniciais)

if 'stands' not in st.session_state:
    st.session_state['stands'] = pd.DataFrame(columns=["Nome do Stand", "Endereço", "Prazo de Locação", "Status"])

if 'centros_custo' not in st.session_state:
    st.session_state['centros_custo'] = pd.DataFrame(columns=["Nome do Centro de Custo", "CNPJ", "Descrição", "Status"])

if 'chamados' not in st.session_state:
    st.session_state['chamados'] = pd.DataFrame(columns=["ID", "Stand", "Descrição", "Status", "Prioridade"])


# --- PÁGINA DE TROCA DE SENHA OBRIGATÓRIA ---
def tela_trocar_senha():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center;'>Atualização de Senha Obrigatória 🔒</h3>", unsafe_allow_html=True)
        st.warning("É o seu primeiro acesso ou sua senha expirou (passou de 90 dias). Por favor, crie uma nova senha de acesso.")
        
        with st.form("form_trocar_senha"):
            nova_senha = st.text_input("Nova Senha", type="password")
            conf_senha = st.text_input("Confirme a Nova Senha", type="password")
            submit_senha = st.form_submit_button("Atualizar Senha", use_container_width=True)
            
            if submit_senha:
                if len(nova_senha) < 4:
                    st.error("A senha deve ter pelo menos 4 caracteres.")
                elif nova_senha != conf_senha:
                    st.error("As senhas não coincidem.")
                else:
                    # Atualiza a senha no dataframe de usuários
                    email = st.session_state['usuario_logado']
                    df = st.session_state['usuarios']
                    idx = df[df['Email'] == email].index[0]
                    
                    df.at[idx, 'Senha'] = nova_senha
                    df.at[idx, 'Primeiro_Acesso'] = False
                    df.at[idx, 'Data_Ultima_Senha'] = datetime.date.today()
                    
                    st.session_state['usuarios'] = df
                    st.session_state['precisa_trocar_senha'] = False
                    st.success("Senha atualizada! Redirecionando...")
                    st.rerun()

# --- PÁGINA DE LOGIN ---
def tela_login():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        logo = carregar_logo()
        if logo:
            st.image(logo, use_container_width=True)
            
        st.markdown("<h3 style='text-align: center;'>Acesso Restrito</h3>", unsafe_allow_html=True)
        st.write("") 
        
        with st.form("login_form"):
            user = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                df_users = st.session_state['usuarios']
                # Busca o usuário pelo e-mail e senha
                user_match = df_users[(df_users['Email'] == user) & (df_users['Senha'] == senha)]
                
                if not user_match.empty:
                    st.session_state['autenticado'] = True
                    st.session_state['usuario_logado'] = user
                    
                    # Verificação de segurança (Primeiro Acesso ou Expirou 90 dias)
                    idx = user_match.index[0]
                    primeiro_acesso = user_match.at[idx, 'Primeiro_Acesso']
                    data_senha = user_match.at[idx, 'Data_Ultima_Senha']
                    hoje = datetime.date.today()
                    
                    if primeiro_acesso or (hoje - data_senha).days > 90:
                        st.session_state['precisa_trocar_senha'] = True
                    else:
                        st.session_state['precisa_trocar_senha'] = False
                        
                    st.rerun()
                else:
                    st.error("Credenciais inválidas ou usuário não encontrado.")

# --- MÓDULOS DO SISTEMA ---

def module_painel_gestao():
    st.header("📊 Painel de Gestão (Dashboard)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Chamados Abertos", "12", "-2")
    col2.metric("Lead Time Compras", "4 dias", "1 dia", delta_color="inverse")
    col3.metric("Despesas no Mês", "R$ 145.000", "R$ 12k")
    col4.metric("Ações de MKT Ativas", "3")
    
    st.subheader("Minhas Tarefas (Atribuídas pela Diretoria)")
    tarefas = pd.DataFrame({"Tarefa": ["Aprovar orçamento Stand A", "Revisar escala"], "Prazo": ["Hoje", "Amanhã"], "Status": ["Pendente", "Pendente"]})
    st.dataframe(tarefas, use_container_width=True, hide_index=True)

def module_cadastro():
    st.header("📝 Cadastro Integrado")
    st.info("💡 Dica: Na tabela abaixo, você pode dar um duplo-clique em qualquer item para editar ou clicar nas bordas para excluir uma linha.")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Usuários", "Stands de Vendas", "Centros de Custo", "Itens de Inventário"])
    
    # --- ABA 1: USUÁRIOS ---
    with tab1:
        st.subheader("Gestão de Usuários")
        with st.expander("➕ Novo Usuário"):
            # clear_on_submit=True limpa os dados após salvar
            with st.form("form_novo_usuario", clear_on_submit=True):
                c1, c2 = st.columns(2)
                nome = c1.text_input("Nome e Sobrenome")
                email = c2.text_input("E-mail")
                senha = c1.text_input("Senha Inicial (Usuário deverá trocar)", type="password")
                telefone = c2.text_input("Telefone")
                perfil = c1.selectbox("Perfil", ["Diretor", "Gestor", "Administrativo", "Manutenção"])
                
                if st.form_submit_button("Salvar Usuário"):
                    novo_usuario = pd.DataFrame([{
                        "Nome": nome, "Email": email, "Telefone": telefone, 
                        "Perfil": perfil, "Senha": senha, "Primeiro_Acesso": True, 
                        "Data_Ultima_Senha": datetime.date.today(), "Status": "Ativo"
                    }])
                    st.session_state['usuarios'] = pd.concat([st.session_state['usuarios'], novo_usuario], ignore_index=True)
                    st.success(f"Usuário {nome} cadastrado! (Os campos foram limpos)")
                    st.rerun()
        
        # Tabela Editável (st.data_editor)
        st.session_state['usuarios'] = st.data_editor(st.session_state['usuarios'], num_rows="dynamic", use_container_width=True, key="edit_user")

    # --- ABA 2: STANDS DE VENDAS ---
    with tab2:
        st.subheader("Stands e Projetos")
        with st.expander("➕ Novo Stand de Vendas"):
            with st.form("form_novo_stand", clear_on_submit=True):
                nome_stand = st.text_input("Nome do Stand")
                endereco = st.text_input("Endereço Completo")
                prazo = st.text_input("Prazo de locação do espaço (Ex: 12 meses)")
                
                if st.form_submit_button("Salvar Stand"):
                    novo_stand = pd.DataFrame([{"Nome do Stand": nome_stand, "Endereço": endereco, "Prazo de Locação": prazo, "Status": "Ativo"}])
                    st.session_state['stands'] = pd.concat([st.session_state['stands'], novo_stand], ignore_index=True)
                    st.success(f"Stand '{nome_stand}' cadastrado com sucesso!")
                    st.rerun()
                    
        # Tabela Editável
        st.session_state['stands'] = st.data_editor(st.session_state['stands'], num_rows="dynamic", use_container_width=True, key="edit_stand")

    # --- ABA 3: CENTROS DE CUSTO ---
    with tab3:
        st.subheader("Centros de Custo")
        with st.expander("➕ Novo Centro de Custo"):
            with st.form("form_novo_cc", clear_on_submit=True):
                nome_cc = st.text_input("Nome do Centro de Custo (Ex: SPE NOVA IGUACU)")
                cnpj_cc = st.text_input("CNPJ")
                desc_cc = st.text_input("Descrição / Finalidade")
                
                if st.form_submit_button("Salvar Centro de Custo"):
                    novo_cc = pd.DataFrame([{"Nome do Centro de Custo": nome_cc, "CNPJ": cnpj_cc, "Descrição": desc_cc, "Status": "Ativo"}])
                    st.session_state['centros_custo'] = pd.concat([st.session_state['centros_custo'], novo_cc], ignore_index=True)
                    st.success(f"Centro de Custo '{nome_cc}' cadastrado!")
                    st.rerun()
                    
        # Tabela Editável
        st.session_state['centros_custo'] = st.data_editor(st.session_state['centros_custo'], num_rows="dynamic", use_container_width=True, key="edit_cc")

    with tab4:
        st.subheader("Inventário Inicial")
        st.info("Esta lista será populada a partir das aprovações de compras (imobilizados).")

def module_manutencao():
    st.header("🔧 Manutenção")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Abertura de Chamado")
        with st.form("form_os", clear_on_submit=True):
            lista_stands = st.session_state['stands']['Nome do Stand'].tolist()
            if not lista_stands:
                lista_stands = ["Nenhum stand cadastrado"]
                
            stand = st.selectbox("Stand", lista_stands)
            descricao = st.text_area("Descrição do Problema")
            prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta", "Urgente"])
            if st.form_submit_button("Abrir OS"):
                st.success("Chamado aberto!")
    with col2:
        st.subheader("Backlog de Manutenção")
        st.dataframe(st.session_state['chamados'], use_container_width=True)

def module_financeiro():
    st.header("💰 Financeiro")

def module_compras():
    st.header("🛒 Compras")

def module_inventario():
    st.header("📦 Inventário Patrimonial")

def module_marketing():
    st.header("🎯 Marketing")

def module_escala():
    st.header("👥 Escala do Time")

# --- CONTROLADOR PRINCIPAL ---
def main():
    if not st.session_state['autenticado']:
        tela_login()
    elif st.session_state['precisa_trocar_senha']:
        tela_trocar_senha()
    else:
        with st.sidebar:
            logo = carregar_logo()
            if logo:
                st.image(logo, use_container_width=True)
            st.divider()
            st.markdown("### 🏢 Departamentos")
            
            modulos = ["Painel de Gestão", "Cadastro", "Manutenção", "Financeiro", "Compras", "Inventário", "Marketing", "Escala do Time"]
            
            for mod in modulos:
                tipo_botao = "primary" if st.session_state['pagina_atual'] == mod else "secondary"
                if st.button(mod, use_container_width=True, type=tipo_botao):
                    st.session_state['pagina_atual'] = mod
                    st.rerun()
            
            st.divider()
            if st.button("Sair", use_container_width=True):
                st.session_state['autenticado'] = False
                st.session_state['pagina_atual'] = "Painel de Gestão"
                st.rerun()
                
        pagina = st.session_state['pagina_atual']
        if pagina == "Painel de Gestão": module_painel_gestao()
        elif pagina == "Cadastro": module_cadastro()
        elif pagina == "Manutenção": module_manutencao()
        elif pagina == "Financeiro": module_financeiro()
        elif pagina == "Compras": module_compras()
        elif pagina == "Inventário": module_inventario()
        elif pagina == "Marketing": module_marketing()
        elif pagina == "Escala do Time": module_escala()

if __name__ == "__main__":
    main()
