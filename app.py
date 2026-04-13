import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime, date
import calendar
import os
import base64

st.set_page_config(
    page_title="Gestão Integrada Omega & Raphson",
    layout="wide",
    page_icon="🏗️",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.main { background: linear-gradient(135deg, #f0f4ff 0%, #fafbff 100%); min-height: 100vh; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1400px; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; margin: 0.75rem 0; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] label {
    color: #94a3b8 !important; font-size: 0.7rem !important;
    font-weight: 600 !important; text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
.menu-label {
    color: #64748b !important; font-size: 0.65rem !important;
    font-weight: 700 !important; text-transform: uppercase !important;
    letter-spacing: 0.12em !important; padding: 0.5rem 0 0.25rem 0; display: block;
}
.user-footer {
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 12px 14px; margin-top: 8px;
}
.user-name { color: #f1f5f9 !important; font-weight: 600; font-size: 0.88rem; }
.user-level { color: #64748b !important; font-size: 0.75rem; }
h1 { color: #0f172a !important; font-weight: 800 !important; font-size: 1.85rem !important; letter-spacing: -0.02em; margin-bottom: 0.15rem !important; }
h2 { color: #1e293b !important; font-weight: 700 !important; font-size: 1.3rem !important; }
h3 { color: #334155 !important; font-weight: 600 !important; font-size: 1.05rem !important; }
.page-header {
    background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 50%, #2563eb 100%);
    border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 1.75rem;
    display: flex; align-items: center; gap: 1rem;
    box-shadow: 0 8px 32px rgba(30,58,138,0.25);
}
.page-header-icon { font-size: 2.2rem; line-height: 1; }
.page-header-title { color: #ffffff !important; font-size: 1.6rem !important; font-weight: 800 !important; margin: 0 !important; }
.page-header-sub { color: rgba(255,255,255,0.72) !important; font-size: 0.88rem; margin-top: 2px; }
[data-testid="stMetric"] {
    background: #ffffff !important; border-radius: 14px !important;
    padding: 1.25rem 1.5rem !important; box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    border: 1px solid #e2e8f0 !important; border-top: 4px solid #3b82f6 !important;
    transition: transform 0.2s, box-shadow 0.2s;
}
[data-testid="stMetric"]:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(59,130,246,0.15) !important; }
[data-testid="stMetricLabel"] { font-size: 0.78rem !important; font-weight: 600 !important; color: #64748b !important; text-transform: uppercase; }
[data-testid="stMetricValue"] { font-size: 2rem !important; font-weight: 800 !important; color: #0f172a !important; }
[data-testid="stForm"] {
    background: #ffffff; border-radius: 16px; padding: 1.75rem;
    border: 1px solid #e2e8f0; box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input {
    border-radius: 10px !important; border: 1.5px solid #e2e8f0 !important; font-size: 0.9rem !important;
}
.stButton > button {
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.88rem !important; padding: 0.55rem 1.25rem !important;
    transition: all 0.2s !important; border: none !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(37,99,235,0.35) !important; }
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #f1f5f9; border-radius: 12px; padding: 4px; gap: 4px; border-bottom: none !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 9px !important; font-weight: 600 !important; font-size: 0.85rem !important;
    color: #64748b !important; padding: 0.45rem 1.1rem !important; border: none !important; background: transparent !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #ffffff !important; color: #1d4ed8 !important; box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; }
[data-testid="stAlert"] { border-radius: 12px !important; border: none !important; font-weight: 500; }
[data-testid="stExpander"] { background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0 !important; }
hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.25rem 0; }
.custom-card {
    background: #ffffff; border-radius: 14px; padding: 1.25rem 1.5rem;
    border: 1px solid #e2e8f0; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 1rem;
}
.os-card {
    background: #ffffff; border-radius: 14px; padding: 1.25rem 1.5rem;
    border: 1px solid #e2e8f0; border-left: 5px solid #3b82f6;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 1rem;
}
.os-card-alta { border-left-color: #ef4444 !important; }
.os-card-media { border-left-color: #f59e0b !important; }
.os-card-baixa { border-left-color: #22c55e !important; }
.status-badge {
    display: inline-block; padding: 3px 12px; border-radius: 20px;
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.03em;
}
.badge-pendente { background: #fef3c7; color: #92400e; }
.badge-andamento { background: #dbeafe; color: #1e40af; }
.badge-material { background: #ede9fe; color: #5b21b6; }
.badge-concluido { background: #dcfce7; color: #166534; }
.badge-cancelado { background: #fee2e2; color: #991b1b; }
.login-title { text-align: center; color: #0f172a !important; font-size: 1.5rem !important; font-weight: 800 !important; }
.login-sub { text-align: center; color: #64748b; font-size: 0.9rem; margin-bottom: 1.5rem; }
.foto-label { font-size: 0.78rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }
@media (max-width: 768px) {
    .block-container { padding: 1rem 1rem 2rem !important; }
    .page-header { padding: 1rem 1.25rem; border-radius: 12px; }
    .page-header-title { font-size: 1.2rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.5rem !important; }
    h1 { font-size: 1.4rem !important; }
    .os-card { padding: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    'autenticado': False,
    'user_logado': '',
    'nivel': 'Leitor',
    'nome_usuario': '',
    'man_form_key': 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =================================
