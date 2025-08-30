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
    "mode": "sandbox",  # troca para "live" quando for produção
    "client_id": st.secrets["PAYPAL_CLIENT_ID"],
    "client_secret": st.secrets["PAYPAL_CLIENT_SECRET"]
})

# --- Funções --- #

def chat_response(prompt, system_prompt, lang="pt"):
    """Gera resposta do chatbot, traduzindo se necessário"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    text = response.choices[0].message.content

    # Traduzir apenas se idioma != português
    if lang != "pt":
        text = translate_text(text, lang)

    return text

def translate_text(text, target_lang):
    """Traduz texto para o idioma escolhido (rápido e leve)"""
    if target_lang == "pt":
        return text
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"És um tradutor profissional. Traduz para {target_lang} sem perder o tom emocional."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

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
                "items": [{"name": descricao, "sku": str(uuid.uuid4()), "price": str(valor), "currency": "EUR", "quantity": 1}]
            },
            "amount": {"total": str(valor), "currency": "EUR"},
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

# --- Interface --- #

st.title("💘 Conselhos Amorosos com IA")

# Seletor de idioma
idiomas = {"Português": "pt", "Inglês": "en", "Espanhol": "es", "Francês": "fr"}
lang_choice = st.sidebar.selectbox("🌍 Escolhe o idioma:", list(idiomas.keys()))
st.session_state["lang"] = idiomas[lang_choice]

tab1, tab2, tab3, tab4 = st.tabs([
    "Conselhos Amorosos",
    "Sugestões de Respostas",
    "Descobre a tua Alma Gêmea",
    "Descobre como serão os teus Filhos"
])

# --- Tab 1 ---
with tab1:
    st.subheader("Fala comigo sobre os teus sentimentos ❤️")
    if "chat1" not in st.session_state: st.session_state.chat1 = []
    for msg in st.session_state.chat1:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if user_input := st.chat_input("Partilha o que sentes..."):
        # traduz input do user para português se necessário
        prompt = translate_text(user_input, "pt") if st.session_state["lang"] != "pt" else user_input
        st.session_state.chat1.append({"role": "user", "content": user_input})
        with st.chat_message("user"): st.markdown(user_input)
        response = chat_response(prompt, "És um terapeuta empático que dá conselhos amorosos com humanidade.", st.session_state["lang"])
        st.session_state.chat1.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"): st.markdown(response)

# --- Tab 2 ---
with tab2:
    st.subheader("Mostra a mensagem e vamos ajudar 📩")
    if "chat2" not in st.session_state: st.session_state.chat2 = []
    for msg in st.session_state.chat2:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if user_input2 := st.chat_input("Cola aqui a mensagem que recebeste..."):
        prompt2 = translate_text(user_input2, "pt") if st.session_state["lang"] != "pt" else user_input2
        st.session_state.chat2.append({"role": "user", "content": user_input2})
        with st.chat_message("user"): st.markdown(user_input2)
        response2 = chat_response(prompt2, "És um especialista em comunicação amorosa. Ajuda a criar uma resposta empática, romântica e natural.", st.session_state["lang"])
        st.session_state.chat2.append({"role": "assistant", "content": response2})
        with st.chat_message("assistant"): st.markdown(response2)

# --- Tab 3 ---
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
        if link_pagamento: st.markdown(f"[👉 Clica aqui para pagar no PayPal]({link_pagamento})")
        else: st.error("Erro ao criar pagamento. Verifica as credenciais PayPal.")
    if nome and idade and altura and cor_fav and hobbies and profissao and selfie:
        st.info("⚠️ Depois de pagar, vamos gerar a tua alma gêmea!")
        img = Image.open(selfie)
        st.image(img, caption="(Tua selfie enviada)")

# --- Tab 4 ---
with tab4:
    st.subheader("Descobre como serão os teus filhos com ele/ela 👶")
    st.markdown("📸 **Carrega 3 fotos tuas e 3 fotos da outra pessoa**")
    fotos_tuas = st.file_uploader("As tuas 3 fotos", type=["jpg","jpeg","png"], accept_multiple_files=True)
    fotos_dele = st.file_uploader("As 3 fotos dele/dela", type=["jpg","jpeg","png"], accept_multiple_files=True)
    if st.button("Pagar 2€ e Descobrir 👶💕"):
        link_pagamento2 = criar_pagamento(2, "Descobre como serão os teus filhos")
        if link_pagamento2: st.markdown(f"[👉 Clica aqui para pagar no PayPal]({link_pagamento2})")
        else: st.error("Erro ao criar pagamento. Verifica as credenciais PayPal.")
    if fotos_tuas and fotos_dele:
        if len(fotos_tuas) == 3 and len(fotos_dele) == 3:
            st.info("⚠️ Depois do pagamento, vamos gerar imagens realistas dos filhos com base nas fotos enviadas.")
            for f in fotos_tuas + fotos_dele:
                img = Image.open(f)
                st.image(img, width=150)
        else:
            st.warning("Tens de enviar exatamente 3 fotos tuas e 3 fotos dele/dela.")
