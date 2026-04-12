import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Omega & Raphson ERP", layout="wide")

# --- CORREÇÃO VISUAL (LETRAS DO MENU E CORES) ---
st.markdown("""
    <style>
    /* Cor das letras no menu lateral */
    [data-testid="stSidebar"] .st-expanderHeader, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: white !important;
    }
    .main-title { color: #1e3a8a; font-size: 28px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE DADOS ---
def carregar_dados(modulo):
    arquivo = f"dados_{modulo.lower()}.csv"
    if os.path.exists(arquivo):
        return pd.read_csv(arquivo)
    else:
        return pd.DataFrame(columns=['ID', 'Data', 'Stand', 'Tarefa', 'Responsável', 'Escala_Dia', 'Status'])

def salvar_dados(df, modulo):
    df.to_csv(f"dados_{modulo.lower()}.csv", index=False)

# --- BARRA LATERAL ---
st.sidebar.markdown("### 🏢 Omega & Raphson")
# Para a logo: coloque o link de uma imagem online abaixo
st.sidebar.image("https://via.placeholder.com/200x80.png?text=OMEGA+&+RAPHSON", use_container_width=True)

modulo_selecionado = st.sidebar.selectbox(
    "Escolha o Setor:", 
    ["Início", "Manutenção", "Comercial", "Financeiro", "Marketing", "Compras", "Configurações"]
)

st.markdown(f"<div class='main-title'>Omega Inc & Raphson Engenharia</div>", unsafe_allow_html=True)

# --- LÓGICA DE GESTÃO DE TAREFAS (PADRÃO PARA TODOS OS SETORES) ---
if modulo_selecionado in ["Manutenção", "Comercial", "Financeiro", "Marketing", "Compras"]:
    st.header(f"Gestão de Tarefas e Escala: {modulo_selecionado}")
    
    df = carregar_dados(modulo_selecionado)
    
    aba1, aba2 = st.tabs(["📝 Atribuir Tarefa/Escala", "📋 Painel de Gestão"])
    
    with aba1:
        with st.form(f"form_{modulo_selecionado}"):
            col1, col2 = st.columns(2)
            with col1:
                stand = st.selectbox("Stand/Local:", ["Stand Principal", "Stand Jazz", "Stand Live", "Escritório"])
                responsavel = st.text_input("Responsável:")
            with col2:
                # Gestão de Escala de Domingo a Domingo
                dia_escala = st.selectbox("Dia da Escala:", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"])
                status_inicial = "Pendente"
            
            tarefa = st.text_area("Descrição da Tarefa:")
            if st.form_submit_button("Confirmar Atribuição"):
                novo_id = len(df) + 1
                nova_linha = pd.DataFrame([[novo_id, datetime.now().strftime("%d/%m/%Y"), stand, tarefa, responsavel, dia_escala, status_inicial]], 
                                         columns=df.columns)
                df = pd.concat([df, nova_linha], ignore_index=True)
                salvar_dados(df, modulo_selecionado)
                st.success("Tarefa registrada na escala!")
                st.rerun()

    with aba2:
        st.dataframe(df, use_container_width=True, hide_index=True)
        if not df.empty:
            st.divider()
            c1, c2 = st.columns(2)
            id_up = c1.number_input("ID da Tarefa para Editar/Apagar:", min_value=1, step=1)
            acao = c2.selectbox("Ação:", ["Alterar Status", "Apagar Registro"])
            
            if st.button("Executar Alteração"):
                if acao == "Alterar Status":
                    df.loc[df['ID'] == id_up, 'Status'] = "Concluído"
                    st.success("Status atualizado!")
                else:
                    df = df[df['ID'] != id_up]
                    st.warning("Registro removido!")
                salvar_dados(df, modulo_selecionado)
                st.rerun()

# --- MÓDULO DE CONFIGURAÇÕES (ADMIN) ---
elif modulo_selecionado == "Configurações":
    st.header("⚙️ Painel Administrativo")
    st.subheader("Cadastro de Usuários e Alçadas")
    # Aqui futuramente integraremos a lógica de login e permissões
    st.info("Nesta área você poderá definir quem pode 'Apenas Ver' ou 'Editar' cada setor.")
    
    st.subheader("Gerenciar Stands")
    novo_stand = st.text_input("Nome do novo Stand:")
    if st.button("Cadastrar Stand"):
        st.success(f"Stand {novo_stand} adicionado ao sistema!")

else:
    st.write("Selecione um módulo ao lado para gerenciar as operações da Omega & Raphson.")