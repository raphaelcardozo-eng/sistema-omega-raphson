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

# --- INICIALIZAÇÃO DE BANCO DE DADOS TEMPORÁRIO (SESSION STATE) ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'pagina_atual' not in st.session_state:
    st.session_state['pagina_atual'] = "Painel de Gestão"

# Tabelas de Cadastro
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = pd.DataFrame(columns=["Nome", "Email", "Telefone", "Perfil", "Status"])
if 'stands' not in st.session_state:
    st.session_state['stands'] = pd.DataFrame(columns=["Nome do Stand", "Endereço", "Prazo de Locação", "Status"])
if 'centros_custo' not in st.session_state:
    st.session_state['centros_custo'] = pd.DataFrame(columns=["Nome do Centro de Custo", "Descrição", "Status"])

# Outras tabelas
if 'chamados' not in st.session_state:
    st.session_state['chamados'] = pd.DataFrame(columns=["ID", "Stand", "Descrição", "Status", "Prioridade"])

# --- PÁGINA DE LOGIN ---
def tela_login():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        logo = carregar_logo()
        if logo:
            st.image(logo, use_container_width=True)
        else:
            st.warning("⚠️ Imagem 'Image_from_Image.jpg' não encontrada.")
            
        st.markdown("<h3 style='text-align: center;'>Acesso Restrito</h3>", unsafe_allow_html=True)
        st.write("") 
        
        with st.form("login_form"):
            user = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                if user == "raphaelcardozo@raphsonengenharia.com.br" and senha == "1234":
                    st.session_state['autenticado'] = True
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")

# --- MÓDULOS DO SISTEMA ---

def module_painel_gestao():
    st.header("📊 Painel de Gestão (Dashboard)")
    st.write("Visão executiva e indicadores de performance.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Chamados Abertos", value="12", delta="-2")
    col2.metric(label="Lead Time Compras", value="4 dias", delta="1 dia", delta_color="inverse")
    col3.metric(label="Despesas no Mês", value="R$ 145.000", delta="R$ 12k")
    col4.metric(label="Ações de MKT Ativas", value="3")
    
    st.subheader("Minhas Tarefas (Atribuídas pela Diretoria)")
    tarefas = pd.DataFrame({"Tarefa": ["Aprovar orçamento Stand A", "Revisar escala"], "Prazo": ["Hoje", "Amanhã"], "Status": ["Pendente", "Pendente"]})
    st.dataframe(tarefas, use_container_width=True, hide_index=True)

def module_cadastro():
    st.header("📝 Cadastro Integrado")
    tab1, tab2, tab3, tab4 = st.tabs(["Usuários", "Stands de Vendas", "Centros de Custo", "Itens de Inventário"])
    
    # --- ABA 1: USUÁRIOS ---
    with tab1:
        st.subheader("Gestão de Usuários")
        with st.expander("➕ Novo Usuário"):
            with st.form("form_novo_usuario"):
                c1, c2 = st.columns(2)
                nome = c1.text_input("Nome e Sobrenome")
                email = c2.text_input("E-mail")
                perfil = c1.selectbox("Perfil", ["Diretor", "Gestor", "Administrativo", "Manutenção"])
                telefone = c2.text_input("Telefone")
                if st.form_submit_button("Salvar Usuário"):
                    # Salvando na tabela
                    novo_usuario = pd.DataFrame([{"Nome": nome, "Email": email, "Telefone": telefone, "Perfil": perfil, "Status": "Ativo"}])
                    st.session_state['usuarios'] = pd.concat([st.session_state['usuarios'], novo_usuario], ignore_index=True)
                    st.success(f"Usuário {nome} cadastrado com sucesso!")
                    st.rerun() # Atualiza a página para mostrar na tabela
        
        # Exibe a tabela atualizada
        st.dataframe(st.session_state['usuarios'], use_container_width=True)

    # --- ABA 2: STANDS DE VENDAS ---
    with tab2:
        st.subheader("Stands e Projetos")
        with st.expander("➕ Novo Stand de Vendas"):
            with st.form("form_novo_stand"):
                nome_stand = st.text_input("Nome do Stand")
                endereco = st.text_input("Endereço Completo")
                prazo = st.text_input("Prazo de locação do espaço (Ex: 12 meses, 30 dias)")
                
                if st.form_submit_button("Salvar Stand"):
                    novo_stand = pd.DataFrame([{"Nome do Stand": nome_stand, "Endereço": endereco, "Prazo de Locação": prazo, "Status": "Ativo"}])
                    st.session_state['stands'] = pd.concat([st.session_state['stands'], novo_stand], ignore_index=True)
                    st.success(f"Stand '{nome_stand}' cadastrado com sucesso!")
                    st.rerun()
                    
        st.dataframe(st.session_state['stands'], use_container_width=True)

    # --- ABA 3: CENTROS DE CUSTO ---
    with tab3:
        st.subheader("Centros de Custo")
        with st.expander("➕ Novo Centro de Custo"):
            with st.form("form_novo_cc"):
                nome_cc = st.text_input("Nome do Centro de Custo (Ex: CC-Obras, CC-Marketing)")
                desc_cc = st.text_input("Descrição / Finalidade")
                
                if st.form_submit_button("Salvar Centro de Custo"):
                    novo_cc = pd.DataFrame([{"Nome do Centro de Custo": nome_cc, "Descrição": desc_cc, "Status": "Ativo"}])
                    st.session_state['centros_custo'] = pd.concat([st.session_state['centros_custo'], novo_cc], ignore_index=True)
                    st.success(f"Centro de Custo '{nome_cc}' cadastrado com sucesso!")
                    st.rerun()
                    
        st.dataframe(st.session_state['centros_custo'], use_container_width=True)

    # --- ABA 4: INVENTÁRIO ---
    with tab4:
        st.subheader("Inventário Inicial")
        st.info("Aqui faremos a listagem dos itens imobilizados vinculados aos Centros de Custo.")

def module_manutencao():
    st.header("🔧 Manutenção")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Abertura de Chamado")
        with st.form("form_os"):
            # Puxando a lista de stands cadastrados dinamicamente
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
        st.button("Solicitar Material ao Setor de Compras 📦")

def module_financeiro():
    st.header("💰 Financeiro")
    st.write("Controle de pagamentos, conciliação e custos de operação.")

def module_compras():
    st.header("🛒 Compras")
    st.metric(label="SLA Médio de Atendimento", value="4.2 Dias")

def module_inventario():
    st.header("📦 Inventário Patrimonial")
    st.dataframe(pd.DataFrame(columns=["Código", "Item", "Valor", "Centro de Custo", "Data"]), use_container_width=True)

def module_marketing():
    st.header("🎯 Marketing")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Calendário de Ações")
        st.date_input("Selecione uma data:", datetime.date.today())
    with col2:
        st.metric(label="Custo em Campanhas", value="R$ 45.000")

def module_escala():
    st.header("👥 Escala do Time")
    st.success("Você está escalado(a) para o turno das 08h às 18h.")
    st.checkbox("Revisar contratos de fornecedores (Atribuído por: Diretoria)")

# --- CONTROLADOR PRINCIPAL ---
def main():
    if not st.session_state['autenticado']:
        tela_login()
    else:
        with st.sidebar:
            logo = carregar_logo()
            if logo:
                st.image(logo, use_container_width=True)
            st.divider()
            st.markdown("### 🏢 Departamentos")
            
            modulos = [
                "Painel de Gestão", 
                "Cadastro", 
                "Manutenção", 
                "Financeiro", 
                "Compras", 
                "Inventário", 
                "Marketing", 
                "Escala do Time"
            ]
            
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
        if pagina == "Painel de Gestão":
            module_painel_gestao()
        elif pagina == "Cadastro":
            module_cadastro()
        elif pagina == "Manutenção":
            module_manutencao()
        elif pagina == "Financeiro":
            module_financeiro()
        elif pagina == "Compras":
            module_compras()
        elif pagina == "Inventário":
            module_inventario()
        elif pagina == "Marketing":
            module_marketing()
        elif pagina == "Escala do Time":
            module_escala()

if __name__ == "__main__":
    main()
