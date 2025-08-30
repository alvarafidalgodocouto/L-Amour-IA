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
    "mode": "sandbox",  # trocar para "live" quando for produção
    "client_id": st.secrets["PAYPAL_CLIENT_ID"],
    "client_secret": st.secrets["PAYPAL_CLIENT_SECRET"]
})

# --- Tradutor leve com cache ---
@st.cache_data
def traduzir_texto(texto, idioma_destino="PT"):
    if idioma_destino == "PT":
        return texto
    prompt = f"Traduz o seguinte texto para {idioma_destino} mantendo o mesmo significado e tom:\n\n{texto}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- Função de chat com IA ---
def chat_response(prompt, system_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# --- Função para criar pagamento PayPal ---
def criar_pagamento(valor, descricao, return_url="https://www.google.com", cancel_url="https://www.google.com"):
    pagamento = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url
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
            "amount": {"total": str(valor), "currency": "EUR"},
            "description": descricao
        }]
    })

    if pagamento.create():
        return pagamento.links[1].href
    else:
        return None

# --- Seleção de idioma ---
idioma = st.selectbox("Escolhe o idioma 🌐", options=["PT", "EN", "ES", "FR", "DE"])

# --- UI ---
st.title(traduzir_texto("💘 Conselhos Amorosos com IA", idioma))

tab1, tab2, tab3, tab4 = st.tabs([
    traduzir_texto("Precisas de um bom conselho para a tua relação?", idioma),
    traduzir_texto("Não sabes o que responder? Cola a mensagem aqui que te ajudamos!", idioma),
    traduzir_texto("Descobre quem é a tua alma gêmea", idioma),
    traduzir_texto("Descobre como serão os teus filhos com ele/ela", idioma)
])

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

        response = chat_response(user_input, traduzir_texto(
            "És um terapeuta empático que dá conselhos amorosos com humanidade.", idioma))
        st.session_state.chat1.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

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

        response2 = chat_response(user_input2, traduzir_texto(
            "És um especialista em comunicação amorosa. Ajuda a criar uma resposta empática, romântica e natural.", idioma))
        st.session_state.chat2.append({"role": "assistant", "content": response2})
        with st.chat_message("assistant"):
            st.markdown(response2)

# --- Tab 3: Alma Gêmea ---
with tab3:
    st.subheader(traduzir_texto("Descobre quem é a tua alma gêmea ✨", idioma))
    nome = st.text_input(traduzir_texto("Qual é o teu nome?", idioma))
    idade = st.number_input(traduzir_texto("Qual é a tua idade?", idioma), min_value=16, max_value=100, step=1)
    altura = st.text_input(traduzir_texto("Qual é a tua altura?", idioma))
    cor_fav = st.text_input(traduzir_texto("Qual é a tua cor favorita?", idioma))
    hobbies = st.text_area(traduzir_texto("Quais são os teus hobbies?", idioma))
    profissao = st.text_input(traduzir_texto("Qual é a tua profissão?", idioma))
    selfie = st.file_uploader(traduzir_texto("Envia uma selfie 📷", idioma), type=["jpg", "png", "jpeg"])

    if st.button(traduzir_texto("Pagar 1€ e Gerar Alma Gêmea 💕", idioma)):
        link_pagamento = criar_pagamento(1, "Desenho da Alma Gêmea")
        if link_pagamento:
            st.markdown(f"[👉 Clica aqui para pagar no PayPal e receber a tua alma gêmea]({link_pagamento})")
        else:
            st.error(traduzir_texto("Erro ao criar pagamento. Verifica as credenciais PayPal.", idioma))

    if nome and idade and altura and cor_fav and hobbies and profissao and selfie:
        st.info(traduzir_texto("⚠️ Depois de pagar, vamos gerar a tua alma gêmea!", idioma))
        img = Image.open(selfie)
        st.image(img, caption="(Tua selfie enviada)")

# --- Tab 4: Filhos ---
with tab4:
    st.subheader(traduzir_texto("Descobre como serão os teus filhos com ele/ela 👶", idioma))
    st.markdown(traduzir_texto("📸 Carrega 3 fotos tuas e 3 fotos da outra pessoa", idioma))

    fotos_tuas = st.file_uploader(traduzir_texto("As tuas 3 fotos", idioma), type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    fotos_dele = st.file_uploader(traduzir_texto("As 3 fotos dele/dela", idioma), type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if st.button(traduzir_texto("Pagar 2€ e Descobrir 👶💕", idioma)):
        link_pagamento2 = criar_pagamento(2, "Descobre como serão os teus filhos")
        if link_pagamento2:
            st.markdown(f"[👉 Clica aqui para pagar no PayPal e ver como serão os vossos filhos]({link_pagamento2})")
        else:
            st.error(traduzir_texto("Erro ao criar pagamento. Verifica as credenciais PayPal.", idioma))

    if fotos_tuas and fotos_dele:
        if len(fotos_tuas) == 3 and len(fotos_dele) == 3:
            st.info(traduzir_texto("⚠️ Depois do pagamento, vamos gerar imagens realistas dos filhos com base nas fotos enviadas.", idioma))
            for f in fotos_tuas + fotos_dele:
                img = Image.open(f)
                st.image(img, width=150)
        else:
            st.warning(traduzir_texto("Tens de enviar exatamente 3 fotos tuas e 3 fotos dele/dela.", idioma))

