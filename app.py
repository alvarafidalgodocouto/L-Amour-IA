import streamlit as st
from openai import OpenAI
from PIL import Image
import paypalrestsdk
import uuid

# Config inicial
st.set_page_config(page_title="App Conselhos Amorosos 💕", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
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
    return response.choices[0].message["content"]

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
            "item_list": {
                "items": [{
                    "name": descricao,
                    "sku": str(uuid.uuid4()),
                    "price": str(valor),
                    "currency": "EUR",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(valor),
                "currency": "EUR"
            },
            "description": descricao
        }]
    })

    if pagamento.create():
        for link in pagamento.links:
            if link.rel == "approval_url":
                return link.href
        return None
    else:
        return None

# UI
st.title("💘 Conselhos Amorosos com IA")

tab1, tab2, tab3, tab4 = st.tabs([
    "Precisas de um bom conselho para a tua relação?",
    "Não sabes o que responder? Cola a mensagem aqui que te ajudamos!",
    "Descobre quem é a tua alma gêmea",
    "Descobre como serão os teus filhos com ele/ela"
])

# --- Tab 1: Conselhos Amorosos ---
with tab1:
    st.subheader("Fala comigo sobre os teus sentimentos ❤️")
    if "chat1" not in st.session_state:
        st.session_state.chat1 = []

    for msg in st.session_state.chat1:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Partilha o que sentes..."):
        st.session_state.chat1.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        response = chat_response(user_input, "És um terapeuta empático que dá conselhos amorosos com humanidade.")
        st.session_state.chat1.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# --- Tab 2: Sugestões de respostas ---
with tab2:
    st.subheader("Mostra a mensagem e vamos ajudar 📩")
    if "chat2" not in st.session_state:
        st.session_state.chat2 = []

    for msg in st.session_state.chat2:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input2 := st.chat_input("Cola aqui a mensagem que recebeste..."):
        st.session_state.chat2.append({"role": "user", "content": user_input2})
        with st.chat_message("user"):
            st.markdown(user_input2)

        response2 = chat_response(user_input2, "És um especialista em comunicação amorosa. Ajuda a criar uma resposta empática, romântica e natural.")
        st.session_state.chat2.append({"role": "assistant", "content": response2})
        with st.chat_message("assistant"):
            st.markdown(response2)

# --- Tab 3: Alma Gêmea ---
with tab3:
    st.subheader("Descobre quem é a tua alma gêmea ✨")

    nome = st.text_input("Qual é o teu nome?")
    idade = st.number_input("Qual é a tua idade?", min_value=16, max_value=100, step=1)
    altura = st.text_input("Qual é a tua altura?")
    cor_fav = st.text_input("Qual é a tua cor favorita?")
    hobbies = st.text_area("Quais são os teus hobbies?")
    profissao = st.text_input("Qual é a tua profissão?")

    selfie = st.file_uploader("Envia uma selfie 📷", type=["jpg", "png", "jpeg"])

    if st.button("Pagar 1€ e Gerar Alma Gêmea 💕"):
        link_pagamento = criar_pagamento(1, "Desenho da Alma Gêmea")
        if link_pagamento:
            st.markdown(f"[👉 Clica aqui para pagar no PayPal e receber a tua alma gêmea]({link_pagamento})")
        else:
            st.error("Erro ao criar pagamento. Verifica as credenciais PayPal.")

    if nome and idade and altura and cor_fav and hobbies and profissao and selfie:
        st.info("⚠️ Depois de pagar, vamos gerar a tua alma gêmea!")
        img = Image.open(selfie)
        st.image(img, caption="(Tua selfie enviada)")

# --- Tab 4: Filhos ---
with tab4:
    st.subheader("Descobre como serão os teus filhos com ele/ela 👶")

    st.markdown("📸 **Carrega 3 fotos tuas e 3 fotos da outra pessoa**")

    fotos_tuas = st.file_uploader("As tuas 3 fotos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    fotos_dele = st.file_uploader("As 3 fotos dele/dela", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if st.button("Pagar 2€ e Descobrir 👶💕"):
        link_pagamento2 = criar_pagamento(2, "Descobre como serão os teus filhos")
        if link_pagamento2:
            st.markdown(f"[👉 Clica aqui para pagar no PayPal e ver como serão os vossos filhos]({link_pagamento2})")
        else:
            st.error("Erro ao criar pagamento. Verifica as credenciais PayPal.")

    if fotos_tuas and fotos_dele:
        if len(fotos_tuas) == 3 and len(fotos_dele) == 3:
            st.info("⚠️ Depois do pagamento, vamos gerar imagens realistas dos filhos com base nas fotos enviadas.")
            for f in fotos_tuas + fotos_dele:
                img = Image.open(f)
                st.image(img, width=150)
        else:
            st.warning("Tens de enviar exatamente 3 fotos tuas e 3 fotos dele/dela.")
