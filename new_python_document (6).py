import streamlit as st
from openai import OpenAI
from PIL import Image


st.set_page_config(page_title="App Conselhos Amorosos 💕", layout="wide")


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def chat_response(prompt, system_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


st.title("💘 Conselhos Amorosos com IA")

tab1, tab2, tab3 = st.tabs([
    "Precisas de um bom conselho para a tua relação?",
    "Não sabes o que responder? Cola a mensagem aqui que te ajudamos!",
    "Descobre quem é a tua alma gêmea"
])


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


with tab3:
    st.subheader("Descobre quem é a tua alma gêmea ✨")

    nome = st.text_input("Qual é o teu nome?")
    idade = st.number_input("Qual é a tua idade?", min_value=16, max_value=100, step=1)
    altura = st.text_input("Qual é a tua altura?")
    cor_fav = st.text_input("Qual é a tua cor favorita?")
    hobbies = st.text_area("Quais são os teus hobbies?")
    profissao = st.text_input("Qual é a tua profissão?")

    selfie = st.file_uploader("Envia uma selfie 📷", type=["jpg", "png", "jpeg"])

    if st.button("Gerar a tua alma gêmea 💕"):
        if nome and idade and altura and cor_fav and hobbies and profissao and selfie:
            st.success("Obrigado! A tua alma gêmea está a ser criada...")
            st.info("⚠️ Nesta versão demo ainda não estamos a gerar imagens reais. Em breve vais poder receber a tua alma gêmea com IA real!")
            img = Image.open(selfie)
            st.image(img, caption="(Foto enviada por ti)")
        else:
            st.error("Por favor preenche todas as perguntas e envia a selfie.")
