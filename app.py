
import streamlit as st
from openai import OpenAI
from PIL import Image
import paypalrestsdk
import uuid

# Config inicial
st.set_page_config(page_title="App Conselhos Amorosos 💕", layout="wide")

# Cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Configuração PayPal
paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": st.secrets["PAYPAL_CLIENT_ID"],
    "client_secret": st.secrets["PAYPAL_CLIENT_SECRET"]
})

# Função de chat com IA
def chat_response(prompt, system_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Função de tradução
def traduzir_texto(texto, idioma_destino="PT"):
    prompt = f"Traduz o seguinte texto para {idioma_destino} mantendo o mesmo significado e tom:\n\n{texto}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Função para criar pagamento PayPal
def criar_pagamento(valor, descricao):
    pagamento = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "https://www.google.com",
            "cancel_url": "https://www.google.com"
        },
        "transactions": [{
            "item_list": {"items": [{"name": descricao, "sku": str(uuid.uuid4()), "price": str(valor), "currency": "EUR", "quantity": 1}]},
            "amount": {"total": str(valor), "currency": "EUR"},
            "description": descricao
        }]
    })
    if pagamento.create():
        return pagamento.links[1].href
    else:
        return None

# Seleção de idioma
idioma = st.selectbox("Escolhe o idioma 🌐", options=["PT", "EN", "ES", "FR", "DE"])

# UI
st.title(traduzir_texto("💘 Conselhos Amorosos com IA", idioma))
tab1, tab2 = st.tabs([traduzir_texto("Conselhos", idioma), traduzir_texto("Respostas", idioma)])

# --- Tab 1: Conselhos Amorosos ---
with tab1:
    st.subheader(traduzir_texto("Fala comigo sobre os teus sentimentos ❤️", idioma))
    if "chat1" not in st.session_state:
        st.session_state.chat1 = []
    for msg in st.session_state.chat1:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if user_input := st.chat_input(traduzir_texto("Partilha o que sentes...", idioma)):
        st.session_state.chat1.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        response = chat_response(user_input, traduzir_texto("És um terapeuta empático que dá conselhos amorosos com humanidade.", idioma))
        response_trad = traduzir_texto(response, idioma)
        st.session_state.chat1.append({"role": "assistant", "content": response_trad})
        with st.chat_message("assistant"):
            st.markdown(response_trad)

# --- Tab 2: Sugestões de respostas ---
with tab2:
    st.subheader(traduzir_texto("Mostra a mensagem e vamos ajudar 📩", idioma))
    if "chat2" not in st.session_state:
        st.session_state.chat2 = []
    for msg in st.session_state.chat2:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if user_input2 := st.chat_input(traduzir_texto("Cola aqui a mensagem que recebeste...", idioma)):
        st.session_state.chat2.append({"role": "user", "content": user_input2})
        with st.chat_message("user"):
            st.markdown(user_input2)
        response2 = chat_response(user_input2, traduzir_texto("És um especialista em comunicação amorosa. Ajuda a criar uma resposta empática, romântica e natural.", idioma))
        response2_trad = traduzir_texto(response2, idioma)
        st.session_state.chat2.append({"role": "assistant", "content": response2_trad})
        with st.chat_message("assistant"):
            st.markdown(response2_trad)
