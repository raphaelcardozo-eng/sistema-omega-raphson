import streamlit as st
import pandas as pd
import os

# Configuração básica
st.set_page_config(page_title="Sistema Omega & Raphson", layout="wide")

# Inicialização simples de sessão
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

# --- TELA DE LOGIN ---
if not st.session_state['autenticado']:
    st.title("🏗️ Login - Omega & Raphson")
    with st.form("login"):
        user = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.form_submit_button("Entrar"):
            if user == "admin" and senha == "1234":
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")
    st.stop()

# --- AMBIENTE INTERNO ---
st.sidebar.title("Menu")
pagina = st.sidebar.selectbox("Ir para:", ["Dashboard", "Escala", "Sair"])

if pagina == "Sair":
    st.session_state['autenticado'] = False
    st.rerun()

st.title(f"Bem-vindo ao Painel: {pagina}")
st.write("Sistema carregado com sucesso!")
