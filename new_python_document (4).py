import streamlit as st
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFilter
import random

# ----------------------------
# CONFIGURAÇÃO APP
# ----------------------------
st.set_page_config(
    page_title="💘 Conselhos Amorosos IA",
    page_icon="💘",
    layout="centered"
)

APP_TITLE = "💘 Conselhos Amorosos — Chat & Imagens"
st.title(APP_TITLE)
st.caption("App interativa de conselhos amorosos, sugestões de respostas e geração de imagens realistas.")

# ----------------------------
# CHATBOT SIMPLES (tipo ChatGPT)
# ----------------------------
if "chat1" not in st.session_state:
    st.session_state.chat1 = []

if "chat2" not in st.session_state:
    st.session_state.chat2 = []

def responder_conselho(msg):
    respostas = [
        "Percebo como te sentes ❤️. O importante é comunicar com sinceridade.",
        "Isso é normal sentir... tenta dar um passo de cada vez.",
        "Lembra-te: ouvir e validar sentimentos é metade da solução.",
        "Às vezes precisamos apenas de mostrar vulnerabilidade."
    ]
    return random.choice(respostas)

def responder_mensagem(msg):
    respostas = [
        "Podes responder de forma leve: 'Adorei a tua mensagem, fez-me sorrir 😊'",
        "Tenta mostrar interesse: 'Conta-me mais sobre isso?'",
        "Responde com humor, isso aproxima ainda mais!"
    ]
    return random.choice(respostas)

# ----------------------------
# PLACEHOLDER IMAGENS
# ----------------------------
def gerar_retrato_placeholder(label: str) -> Image.Image:
    W, H = 512, 640
    canvas = Image.new("RGB", (W, H), (245, 220, 240))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([(40, 80), (W-40, H-80)], radius=60, fill=(255, 230, 240))
    draw.text((120, H//2), f"{label}\n(placeholder)")
    return canvas.filter(ImageFilter.SMOOTH_MORE)

# ----------------------------
# INTERFACE
# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Conselhos Amorosos",
    "💬 Sugestões de Respostas às Mensagens",
    "🎨 Desenho da Tua Alma Gémea (€1)",
    "👶 Descobre como serão os teus filhos (€2)"
])

# ----------------------------
# TAB 1 — Conselhos Amorosos (chat)
# ----------------------------
with tab1:
    st.subheader("Conversa com a IA sobre os teus sentimentos ❤️")

    for msg in st.session_state.chat1:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Partilha o que sentes..."):
        st.session_state.chat1.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        resposta = responder_conselho(prompt)
        st.session_state.chat1.append({"role": "assistant", "content": resposta})
        with st.chat_message("assistant"):
            st.markdown(resposta)

# ----------------------------
# TAB 2 — Sugestões de Resposta (chat)
# ----------------------------
with tab2:
    st.subheader("Sugestões de respostas às mensagens dele/dela 💌")

    for msg in st.session_state.chat2:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Cola aqui a mensagem que recebeste..."):
        st.session_state.chat2.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        resposta = responder_mensagem(prompt)
        st.session_state.chat2.append({"role": "assistant", "content": resposta})
        with st.chat_message("assistant"):
            st.markdown(resposta)

# ----------------------------
# TAB 3 — Alma Gémea
# ----------------------------
with tab3:
    st.subheader("Desenho da tua Alma Gémea 💘")
    st.info("Preço: €1 (via PayPal)")

    nome = st.text_input("O teu nome")
    idade = st.number_input("A tua idade", min_value=16, max_value=99, step=1)
    selfie = st.file_uploader("Envia a tua selfie", type=["jpg", "png"])

    if st.button("Gerar pré-visualização"):
        if selfie:
            img = gerar_retrato_placeholder("Alma Gémea")
            st.image(img, caption="A tua alma gémea (exemplo)")
        else:
            st.warning("Por favor envia uma selfie.")

    st.markdown("[💳 Pagar com PayPal](https://www.paypal.com/paypalme/teuusername/1)")

# ----------------------------
# TAB 4 — Filhos
# ----------------------------
with tab4:
    st.subheader("Descobre como serão os teus filhos com ele/ela 👶")
    st.info("Preço: €2 (via PayPal)")

    fotos_tuas = st.file_uploader("Envia 3 fotos TUAS", type=["jpg","png"], accept_multiple_files=True)
    fotos_delas = st.file_uploader("Envia 3 fotos DELE/DELA", type=["jpg","png"], accept_multiple_files=True)

    if st.button("Gerar pré-visualização filhos"):
        if len(fotos_tuas) == 3 and len(fotos_delas) == 3:
            img = gerar_retrato_placeholder("Filho(a)")
            st.image(img, caption="Exemplo de como poderia ser um filho(a)")
        else:
            st.warning("Por favor envia exatamente 3 fotos tuas e 3 fotos dele/dela.")

    st.markdown("[💳 Pagar com PayPal](https://www.paypal.com/paypalme/teuusername/2)")
