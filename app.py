
import streamlit as st
from openai import OpenAI
import uuid

# --- Configuração inicial ---
st.set_page_config(page_title="App Conselhos Amorosos 💕", layout="wide")

# --- Cliente OpenAI ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Funções ---
def chat_response(prompt, system_prompt):
    """Gera resposta da OpenAI para o prompt dado."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def traduzir_resposta(texto, idioma_destino="PT"):
    """Traduz respostas dinamicamente (somente quando necessário)."""
    if idioma_destino == "PT":
        return texto
    prompt = f"Traduz o seguinte texto para {idioma_destino} mantendo o mesmo significado e tom:\n\n{texto}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- Textos estáticos por idioma (para carregamento rápido) ---
TEXTOS = {
    "PT": {
        "titulo":"💘 Conselhos Amorosos com IA",
        "tab1":"Conselhos",
        "tab2":"Respostas",
        "tab3":"Alma Gêmea",
        "tab4":"Filhos",
        "input1":"Partilha o que sentes...",
        "input2":"Cola aqui a mensagem que recebeste...",
        "sub1":"Fala comigo sobre os teus sentimentos ❤️",
        "sub2":"Mostra a mensagem e vamos ajudar 📩"
    },
    "EN": {
        "titulo":"💘 Love Advice with AI",
        "tab1":"Advice",
        "tab2":"Replies",
        "tab3":"Soulmate",
        "tab4":"Children",
        "input1":"Share your feelings...",
        "input2":"Paste the message you received...",
        "sub1":"Talk to me about your feelings ❤️",
        "sub2":"Show the message and let's help 📩"
    }
}

# --- Seleção de idioma ---
idioma = st.selectbox("Escolhe o idioma 🌐", options=list(TEXTOS.keys()))
textos = TEXTOS[idioma]

# --- Interface ---
st.title(textos["titulo"])
tab1, tab2, tab3, tab4 = st.tabs([textos["tab1"], textos["tab2"], textos["tab3"], textos["tab4"]])

# --- Tab 1: Conselhos Amorosos ---
with tab1:
    st.subheader(textos["sub1"])
    if "chat1" not in st.session_state:
        st.session_state.chat1 = []
    for msg in st.session_state.chat1:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if user_input := st.chat_input(textos["input1"]):
        st.session_state.chat1.append({"role":"user","content":user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        response = chat_response(user_input,"És um terapeuta empático que dá conselhos amorosos com humanidade.")
        response_trad = traduzir_resposta(response, idioma)
        st.session_state.chat1.append({"role":"assistant","content":response_trad})
        with st.chat_message("assistant"):
            st.markdown(response_trad)

# --- Tab 2: Sugestões de respostas ---
with tab2:
    st.subheader(textos["sub2"])
    if "chat2" not in st.session_state:
        st.session_state.chat2 = []
    for msg in st.session_state.chat2:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if user_input2 := st.chat_input(textos["input2"]):
        st.session_state.chat2.append({"role":"user","content":user_input2})
        with st.chat_message("user"):
            st.markdown(user_input2)
        response2 = chat_response(user_input2,"És um especialista em comunicação amorosa. Ajuda a criar uma resposta empática, romântica e natural.")
        response2_trad = traduzir_resposta(response2, idioma)
        st.session_state.chat2.append({"role":"assistant","content":response2_trad})
        with st.chat_message("assistant"):
            st.markdown(response2_trad)

# --- Tab 3: Alma Gêmea ---
with tab3:
    st.write("Tab 3: Alma Gêmea – a implementar lógica para descobrir sua alma gêmea.")

# --- Tab 4: Filhos ---
with tab4:
    st.write("Tab 4: Filhos – a implementar lógica para prever como serão os filhos.")
