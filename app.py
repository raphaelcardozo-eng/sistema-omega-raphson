# --- 2. TELA DE ENTRADA / LOGIN ---
if not st.session_state['autenticado']:
    st.write("<br>", unsafe_allow_html=True)
    
    # CENTRALIZAÇÃO DA NOVA LOGO UNIFICADA
    col_central, col_logo, col_vazia = st.columns([1, 2, 1])
    
    with col_logo:
        try:
            # Substitua 'NOME_DA_SUA_IMAGEM.png' pelo nome do arquivo que você vai subir
            nova_logo = Image.open("logo_composta.png") 
            st.image(nova_logo, use_container_width=True)
        except:
            st.info("📌 Carregando nova identidade visual...")

    # Título atualizado conforme sua solicitação anterior
    st.markdown("<h1 style='text-align: center;'>Gestão Integrada Omega Inc & Raphson Engenharia</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Bem-vindo ao portal administrativo. Identifique-se para continuar.</p>", unsafe_allow_html=True)
    
    # ... (restante do código do formulário de login)
