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
        return None # Retorna None se a imagem não for encontrada para não quebrar o app

# --- INICIALIZAÇÃO DE DADOS MOCK (MEMÓRIA TEMPORÁRIA) ---
# Isso simula um banco de dados para podermos testar a interface
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = pd.DataFrame(columns=["Nome", "Email", "Perfil", "Status"])
if 'chamados' not in st.session_state:
    st.session_state['chamados'] = pd.DataFrame(columns=["ID", "Stand", "Descrição", "Status", "Prioridade"])

# --- PÁGINA DE LOGIN ---
def tela_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo = carregar_logo()
        if logo:
            st.image(logo, use_container_width=True)
        else:
            st.warning("⚠️ Imagem 'Image_from_Image.jpg' não encontrada na pasta.")
            
        st.markdown("<h2 style='text-align: center;'>Acesso Restrito</h2>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            user = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                # Login provisório para teste
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
                    st.success(f"Usuário {nome} cadastrado com sucesso! (Simulação)")
        
        st.write("Usuários Ativos:")
        st.dataframe(st.session_state['usuarios'], use_container_width=True)

    with tab2:
        st.subheader("Stands e Projetos")
        st.info("Área para cadastrar nome, endereço, projeto relacionado e centros de custo do stand.")
        
    with tab3:
        st.subheader("Centros de Custo")
        st.info("Estrutura financeira para alocação de despesas e inventário.")

def module_manutencao():
    st.header("🔧 Manutenção")
    st.write("Gestão de Ordens de Serviço (Corretivas e Preventivas).")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Abertura de Chamado")
        with st.form("form_os"):
            stand = st.selectbox("Stand", ["Stand Alpha", "Stand Beta", "Sede"])
            descricao = st.text_area("Descrição do Problema")
            prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta", "Urgente"])
            if st.form_submit_button("Abrir OS"):
                st.success("Chamado aberto e notificado à equipe!")
    
    with col2:
        st.subheader("Backlog de Manutenção")
        st.dataframe(st.session_state['chamados'], use_container_width=True)
        st.button("Solicitar Material ao Setor de Compras 📦")

def module_financeiro():
    st.header("💰 Financeiro")
    st.write("Controle de pagamentos, conciliação e custos de operação.")
    
    st.subheader("Contas a Pagar (Aprovadas por Compras)")
    st.info("Aqui aparecerão os itens cotados e aprovados pela gestão, prontos para lançamento bancário.")
    
    with st.expander("Lançamento Manual (Fora do fluxo)"):
        st.write("Inserir despesas avulsas atreladas a um Centro de Custo.")
        st.text_input("Descrição")
        st.number_input("Valor (R$)", min_value=0.0)
        st.button("Registrar Despesa")

def module_compras():
    st.header("🛒 Compras")
    st.write("Central de Requisições e Cotações.")
    st.metric(label="SLA Médio de Atendimento", value="4.2 Dias")
    
    st.subheader("Backlog de Requisições")
    st.warning("Nenhuma requisição pendente vinda da Manutenção ou Marketing no momento.")

def module_inventario():
    st.header("📦 Inventário Patrimonial")
    st.write("Controle de imobilizados e bens não-consumíveis.")
    st.info("Esta lista será alimentada automaticamente assim que o Financeiro der baixa no pagamento de um item classificado como 'Imobilizado'.")
    st.dataframe(pd.DataFrame(columns=["Código", "Item", "Valor", "Centro de Custo", "Data de Aquisição"]), use_container_width=True)

def module_marketing():
    st.header("🎯 Marketing")
    st.write("Planejamento estratégico, campanhas e ações.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Calendário de Ações (Mês Corrente)")
        d = st.date_input("Selecione uma data para ver as ações:", datetime.date.today())
        st.write(f"Ações planejadas para {d}: Nenhuma ação cadastrada.")
    with col2:
        st.subheader("Indicadores")
        st.metric(label="Custo em Campanhas", value="R$ 45.000")
        st.metric(label="Leads Gerados", value="342")

def module_escala():
    st.header("👥 Escala do Time")
    st.write("Gestão de turnos, tarefas diárias e rotinas.")
    
    st.subheader("Minha Escala Hoje")
    st.success("Você está escalado(a) para o turno das 08h às 18h.")
    
    st.subheader("Minhas Tarefas do Dia")
    st.checkbox("Revisar contratos de fornecedores (Atribuído por: Diretoria)")
    st.checkbox("Validar requisições de compras (Atribuído por: Gestão)")
    
    with st.expander("➕ Registrar Atividade Extra (Proatividade)"):
        st.text_input("O que você realizou fora da rotina padrão?")
        st.button("Registrar")

# --- CONTROLADOR PRINCIPAL DA APLICAÇÃO ---
def main():
    if not st.session_state['autenticado']:
        tela_login()
    else:
        # Layout Interno
        with st.sidebar:
            logo = carregar_logo()
            if logo:
                st.image(logo, use_container_width=True)
            st.divider()
            st.markdown("### Navegação")
            menu = st.radio("Selecione o Módulo:", 
                            ["Painel de Gestão", 
                             "Cadastro", 
                             "Manutenção", 
                             "Financeiro", 
                             "Compras", 
                             "Inventário", 
                             "Marketing", 
                             "Escala do Time",
                             "Sair"])
            
        # Roteamento de Páginas
        if menu == "Painel de Gestão":
            module_painel_gestao()
        elif menu == "Cadastro":
            module_cadastro()
        elif menu == "Manutenção":
            module_manutencao()
        elif menu == "Financeiro":
            module_financeiro()
        elif menu == "Compras":
            module_compras()
        elif menu == "Inventário":
            module_inventario()
        elif menu == "Marketing":
            module_marketing()
        elif menu == "Escala do Time":
            module_escala()
        elif menu == "Sair":
            st.session_state['autenticado'] = False
            st.rerun()

if __name__ == "__main__":
    main()
