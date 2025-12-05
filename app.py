import streamlit as st
import Backend # Importa o seu arquivo backend.py

# 1. Configuração da Aba do Navegador
st.set_page_config(
    page_title="Y - Assistente",
    page_icon="🤖",
    layout="centered"
)

# Título na tela
st.title("🤖 Y (Ípsilon)")
st.caption("Assistente Pessoal do Victor - Powered by Gemini")

# 2. Barra Lateral (Configurações)
with st.sidebar:
    st.header("Cérebro do Y")
    modelo_escolhido = st.radio(
        "Qual versão usar?",
        ["gemini-2.0-flash", "gemini-3.0-pro-preview"],
        index=0 # Padrão é o Flash (0)
    )
    
    st.divider()
    
    # Botão de Reset
    if st.button("Limpar Memória da Tela"):
        st.session_state.messages = []
        st.rerun()

# 3. Inicialização (Roda uma vez ao abrir)
if "chat_session" not in st.session_state:
    # Liga o motor do backend
    st.session_state.chat_session = Backend.iniciar_chat(modelo_escolhido)

# Inicializa o histórico visual se não existir
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Opcional: Se quiser carregar o histórico antigo na tela ao abrir
    historico_antigo = Backend.charge_memory()
    for msg in historico_antigo:
        # Traduz 'model' para 'assistant' pro Streamlit entender
        role = "assistant" if msg["role"] == "model" else "user"
        st.session_state.messages.append({"role": role, "content": msg["parts"][0]})

# 4. Desenha as mensagens antigas na tela
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. O CHAT (Campo de texto)
prompt = st.chat_input("Diga algo para o Y...")

if prompt:
    # A. Mostra o que você digitou
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # B. O Y responde
    with st.chat_message("assistant"):
        # Mostra um "escrevendo..." enquanto carrega
        with st.spinner("Y está pensando..."):
            chat = st.session_state.chat_session
            
            try:
                # 1. Envia pro Google (Backend)
                response = chat.send_message(prompt)
                texto_resposta = response.text
                
                # 2. Calcula custo (Backend)
                info_custo = Backend.calc_cost(response)
                
                # 3. Mostra na tela
                st.markdown(texto_resposta)
                st.caption(f"_{info_custo}_") # Letras miúdas em itálico
                
                # 4. Salva memória (Backend)
                Backend.save_memory(chat.history)
                
                # 5. Salva no visual
                st.session_state.messages.append({"role": "assistant", "content": texto_resposta})
                
            except Exception as e:
                st.error(f"Erro de conexão: {e}")

### Como Rodar (O Grande Momento) 🚀
